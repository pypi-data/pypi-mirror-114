from .units import Units
from ..trajectories.rkffile import RKFTrajectoryFile
from ..core.private import saferun
from .kftools import KFFile
import os

__all__ = ['traj_to_rkf', 'vasp_output_to_ams']

def traj_to_rkf(trajfile,  rkftrajectoryfile):
    """
        Convert ase .traj file to .rkf file. NOTE: The order of atoms (or the number of atoms) cannot change between frames!

        trajfile : str
            path to a .traj file
        rkftrajectoryfile : str 
            path to the output .rkf file (will be created)

        Returns : 2-tuple (coords, cell)
            The final coordinates and cell in angstrom
    """
    from ase.io import read, Trajectory
    traj = Trajectory(trajfile)
    rkfout = RKFTrajectoryFile(rkftrajectoryfile, mode='wb')
    rkfout.store_historydata()
    rkfout.store_mddata()

    # Store the units properly
    mdunits = {}
    mdunits['PotentialEnergy'] = 'hartree'
    mdunits['KineticEnergy'] = 'hartree'
    mdunits['TotalEnergy'] = 'hartree'
    rkfout._set_mdunits(mdunits)

    energy_converter = Units.convert(1.0, 'eV', 'hartree')
    gradients_converter = Units.convert(1.0, 'eV/angstrom', 'hartree/bohr')
    stress_converter = Units.convert(1.0, 'eV/angstrom^3', 'hartree/bohr^3')

    coords, cell = None, None
    try:
        for i,atoms in enumerate(traj):
            if i == 0:
                rkfout.set_elements(atoms.get_chemical_symbols())
            coords = atoms.get_positions() # angstrom
            cell = atoms.get_cell()
            try:
                gradients = -atoms.get_forces()*gradients_converter
            except:
                gradients = None
            try:
                stresstensor = atoms.get_stress(voigt=False)*stress_converter
            except:
                stresstensor = None
            mddata = {}
            try:
                energy = atoms.get_potential_energy()*energy_converter
                mddata['PotentialEnergy'] = energy
            except:
                energy = None

            try:
                kinetic_energy = atoms.get_kinetic_energy()*energy_converter
                mddata['KineticEnergy'] = kinetic_energy
            except:
                kinetic_energy = None

            if 'PotentialEnergy' in mddata and 'KineticEnergy' in mddata:
                mddata['TotalEnergy'] = mddata['PotentialEnergy'] + mddata['KineticEnergy']
            
            if len(mddata) == 0:
                mddata = None

            # Create a historydata dictionary, to go into the History section
            historydata = {}
            if gradients is not None :
                historydata['Gradients'] = gradients
            if stresstensor is not None :
                historydata['StressTensor'] = stresstensor
            if len(historydata) == 0 :
                historydata = None

            rkfout.write_next(coords=coords, cell=cell, historydata=historydata, mddata=mddata)

    finally:
        rkfout.close()


    # the below is needed to be able to load the .rkf file with AMSJob.load_external()
    kf = KFFile(rkftrajectoryfile)
    kf['EngineResults%nEntries'] = 0
    kf['General%user input'] = '\xFF'.join(['Engine External','EndEngine'])

    return coords, cell

def vasp_output_to_ams(vasp_folder, wdir=None, overwrite=False, write_engine_rkf=True):
    """ 
        Converts VASP output (OUTCAR, ...) to AMS output (ams.rkf, vasp.rkf)

        Returns: a string containing the directory where ams.rkf was written

        vasp_folder : str
            path to a directory with an OUTCAR, INCAR, POTCAR etc. files

        wdir : str or None
            directory in which to write the ams.rkf and vasp.rkf files
            If None, a subdirectory "AMSJob" of vasp_folder will be created

        overwrite : bool
            if False, first check if wdir already contains ams.rkf and vasp.rkf, in which case do nothing
            if True, overwrite if exists

        write_engine_rkf : bool
            If True, also write vasp.rkf alongside ams.rkf. The vasp.rkf file will only contain an AMSResults section (energy, gradients, stress tensor). It will not contain the DOS or the band structure.
    """
    if not os.path.isdir(vasp_folder):
        raise ValueError('Directory {} does not exist'.format(vasp_folder))

    outcar = os.path.join(vasp_folder, 'OUTCAR')
    if not os.path.exists(outcar):
        raise ValueError('File {} does not exist, should be an OUTCAR file.'.format(outcar))

    if wdir is None:
        wdir = os.path.join(os.path.dirname(outcar),'AMSJob')
        os.makedirs(wdir, exist_ok=True)

    # exit early if ams.rkf already exists
    if os.path.exists(os.path.join(wdir, 'ams.rkf')) and not overwrite:
        return wdir

    # convert OUTCAR to a .traj file inside wdir
    trajfile = os.path.join(wdir,'outcar.traj')
    if os.path.exists(trajfile):
        os.remove(trajfile)
    cmd = [os.path.join(os.environ.get('AMSBIN'),'amspython'),'-m','ase','convert',outcar,trajfile]
    saferun(cmd)
    if not os.path.exists(os.path.join(wdir,'outcar.traj')):
        raise RuntimeError("Couldn't write outcar.traj in {}".format(wdir))

    # remove the target files first if overwrite
    kffile = os.path.join(wdir, 'ams.rkf')
    enginefile = os.path.join(wdir, 'vasp.rkf')
    if os.path.exists(kffile): 
        if overwrite:
            os.remove(kffile)
        else:
            raise RuntimeError("{} already exists, specify overwrite=True to overwrite".format(kffile))
    if os.path.exists(enginefile): 
        if overwrite:
            os.remove(enginefile)
        else:
            raise RuntimeError("{} already exists, specify overwrite=True to overwrite".format(enginefile))

    # convert the .traj file to ams.rkf
    coords, cell = traj_to_rkf(trajfile, kffile)

    # add extra info to the kffile
    kf = KFFile(kffile, autosave=False)
    if write_engine_rkf:
        enginerkf = KFFile(enginefile, autosave=False)
    try:
        kf['EngineResults%nEntries'] = 1
        kf['EngineResults%Title(1)'] = 'vasp'
        kf['EngineResults%Description(1)'] = 'Standalone VASP run. Data from {}'.format(os.path.abspath(outcar))
        kf['EngineResults%Files(1)'] = 'vasp.rkf'
        kf['General%user input'] = '!VASP'

        # read the INCAR
        incarfile = os.path.join(vasp_folder, 'INCAR')
        userinput = ['!VASP','Engine External', '  Free', '  !INCAR']
        if os.path.exists(incarfile):
            with open(incarfile) as incar:
                for line in incar:
                    line = line.split('!')[0]
                    line = line.split('#')[0]
                    line = line.strip()
                    if line.lower().startswith('end'): # "End" is reserved to end the block
                        line = '!'+line
                    if len(line) > 0:
                        userinput.append('    '+line)
            userinput.append('  !EndINCAR')
        userinput.append('  End') #end of the Free block
        userinput.append('EndEngine')
        kf['General%user input'] = '\xFF'.join(userinput)

        # write engine.rkf
        # copy General, Molecule, InputMolecule from ams.rkf
        if write_engine_rkf:
            for sec in ['General','Molecule','InputMolecule']:
                secdict = kf.read_section(sec)
                for k, v in secdict.items():
                    enginerkf[sec+'%'+k] = v
            nEntries = kf['History%nEntries']
            suffix='({})'.format(nEntries)
            if ('History', 'Energy'+suffix) in kf: enginerkf['AMSResults%Energy'] = kf['History%Energy'+suffix]
            if ('History', 'Gradients'+suffix) in kf: enginerkf['AMSResults%Gradients'] = kf['History%Gradients'+suffix]
            if ('History', 'StressTensor'+suffix) in kf: enginerkf['AMSResults%StressTensor'] = kf['History%StressTensor'+suffix]

    finally:
        kf.save()
        if write_engine_rkf:
            enginerkf.save()

    if os.path.exists(trajfile):
        os.remove(trajfile)

    return wdir


import click
import os 
import shutil 
import subprocess

@click.group()
def cli():
    '''Setups a simulation enviroment for the oxDNA simulation package'''
    pass 


@cli.command()
@click.argument('input_type', type = click.Choice(['mc_relax', 'md_relax', 'md']))
def run(input_type):
    '''Run relax runs:\r
            mc_relax - pre relax run using Montecarlo simulation\r 
            md_relax - relax run MD simulation'''

    if input_type == 'mc_relax':
        click.echo('Starting MC relax run.')
        process = subprocess.Popen(['oxDNA', 'input_pre_relax'], stdout=subprocess.PIPE,  stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        process.wait()
        if  process.returncode:
            print('->','oxDNA', 'input_pre_relax')
            print((stderr.decode("utf-8")).split('\n')[-2])
        click.echo('finished.')
        return
    
    if input_type == 'md_relax':
        click.echo('Starting MD relax run.')
        process = subprocess.Popen(['oxDNA', 'input_cuda_relax'], stdout=subprocess.PIPE,  stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        process.wait()
        if  process.returncode:
            print('->','oxDNA', 'input_cuda_relax')
            print((stderr.decode("utf-8")).split('\n')[-2])
        click.echo('finished.')
        return

    if input_type=='md':
        if not os.path.isfile('last_conf.dat'):
            shutil.copy('relaxed_cuda.dat', 'last_conf.dat')
            
        click.echo('Starting MD simulation.')
        process = subprocess.Popen(['oxDNA', 'input_cuda'],
                                                             stdout=subprocess.PIPE, 
                                                             stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        process.wait()
        if  process.returncode:
            print('->','oxDNA', 'input_cuda')
            print((stderr.decode("utf-8")).split('\n')[-2])
            
        click.echo('finished.')
        return
        




@cli.group ()
def relax():
    '''Create new relaxation enviroment for submitted input type.'''
    pass

@relax.command()
@click.option('--top',      required =True, type=click.Path(exists = True),     help='topology file ')
@click.option('--dat',      required =True, type=click.Path(exists = True),     help='configuration file')
@click.option('--trap',     required=False, type=click.Path(), default=None, help='oxDNA pair trap file') 
@click.option('--outdir', required=False, type=click.Path(),  default='.',       help='output directory')
def oxdna(top, dat, trap, outdir):
    ''' oxDNA configuration relaxation'''
    if outdir != '.':
        os.mkdir(outdir)
    
    #list of input files usually required to relax an oxDNA input file
    init_relax_files = [
        'init_files/input_pre_relax',
        'init_files/input_cuda',
        'init_files/input_cuda_relax',
        'init_files/oxDNA2_sequence_dependent_parameters.txt'
    ]
    #location of the script directory
    dir_path = os.path.dirname(os.path.realpath(__file__))
    for ini_file in init_relax_files:
        shutil.copy(os.path.join(dir_path,ini_file), outdir)
    #handle trap file 
    if trap:
        shutil.copy(trap, os.path.join(outdir, 'pair_trap.txt'))
    #copy the actual configuration over
    #init conf directory     
    init_conf_dir = os.path.join(outdir,'init_conf')
    os.mkdir(init_conf_dir)
    shutil.copy(top, init_conf_dir)
    shutil.copy(dat, init_conf_dir)
    #starting config
    shutil.copy(top, os.path.join(outdir,'init.top'))
    shutil.copy(dat, os.path.join(outdir,'init.dat'))

#@relax.command()
#@click.option('--conf', required=True, type=str, help='cando input file ')
#@click.option('--box', required=False, default=100, help='simulation box size')
#def cando(conf, box):
#    ''' Cando configuration relaxation. '''
#    click.echo(conf)
#    click.echo(box)
#    pass
#
#@relax.command()
#@click.option('--design', required=True, type=str, help='tiamat json file')
#@click.option('--v', required=False, default=2, help='tiamat version')
#@click.option('--default_base', required=False, default='R', help='default base to use for unassigned bases')
#def tiamat(design, v, default_base):
#    ''' Tiamat file relaxation. '''
#    pass
#
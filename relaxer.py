import click
import os 
import shutil 

@click.group()
def cli():
    '''Setups a simulation enviroment for the oxDNA simulation package'''
    pass 


@cli.group ()
def relax():
    '''Create new relaxation enviroment for submitted input type.'''
    pass

@relax.command()
@click.option('--top',      required =True, type=click.Path(exists = True),  help='topology file ')
@click.option('--dat',      required =True, type=click.Path(exists = True),  help='configuration file')
@click.option('--outdir', required=False, type=click.Path(),  default='.',    help='output directory')
def oxdna(top, dat, outdir):
    ''' oxDNA configuration relaxation'''
    if outdir != '.':
        os.mkdir(outdir)
    #list of input files usually required to relax an oxDNA input file
    init_files = [
        'init_files/input_relax',
        'init_files/input_CUDA',
        'init_files/input_cuda_continue_relax',
        'init_files/oxDNA2_sequence_dependent_parameters.txt'
    ]
    #location of the script directory
    dir_path = os.path.dirname(os.path.realpath(__file__))
    for ini_file in init_files:
        shutil.copy(os.path.join(dir_path,ini_file), outdir)

    #copy the actual configuration over
    shutil.copy(top, outdir)
    shutil.copy(dat, outdir)
    
    


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
import ftsa.cli.modules.install_upgrade_parser as iup
import ftsa.cli.modules.run_report_parser as rep
import ftsa.cli.modules.init_parser as ini

from argparse import ArgumentParser


def main():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()

    ''' Install parser '''
    install_parser = subparsers.add_parser('install', help='Installs all framework dependencies.')
    install_parser.set_defaults(handler=iup.install)

    ''' Upgrade parser '''
    upgrade_parser = subparsers.add_parser('upgrade', help='Upgrades all framework dependencies.')
    upgrade_parser.set_defaults(handler=iup.upgrade)

    ''' Uninstall parser '''
    uninstall_parser = subparsers.add_parser('uninstall', help='Uninstalls all framework dependencies.')
    uninstall_parser.set_defaults(handler=iup.uninstall)

    ''' Report parser '''
    report_parser = subparsers.add_parser('report', help='Runs tests using Docker engine, recording (in case of '
                                                         '*web* ui) execution videos and generating execution '
                                                         'result report.')
    # report_parser.add_argument('-p', '--parallel', help='Number of parallel instances. Ex: 2 (two) etc.')
    report_parser.add_argument('-i', '--include', action='append',
                               help='Includes a tag to the execution. Ex: -i all')
    report_parser.add_argument('-e', '--exclude', action='append',
                               help='Excludes a tag of the execution. Ex: -e fe')
    report_parser.add_argument('-nd', '--nodocker', action='store_true', help='Docker execution ignored.')
    report_parser.set_defaults(handler=rep.report)

    ''' Docker Report parser'''
    docker_report_parser = subparsers.add_parser('docker-report', help='Runs tests using an external docker engine')
    docker_report_parser.add_argument('-i', '--include', action='append',
                                      help='Includes a tag to the execution. Ex: -i all')
    docker_report_parser.add_argument('-e', '--exclude', action='append',
                                      help='Excludes a tag of the execution. Ex: -e fe')
    docker_report_parser.add_argument('-n', '--net', action='append',
                                      help='Informs docker network (grid) name. '
                                           'Default: YYYYMMDD_grid (YYYY-year, MM-month, DD-day)')
    docker_report_parser.add_argument('-c', '--container', action='append',
                                      help='Informs the docker execution container name. '
                                           'Default: YYYYMMDD_execution_robot (YYYY-year, MM-month, DD-day)')
    docker_report_parser.add_argument('-p', '--pull', action='store_true',
                                      help='pulls the container image from Docker Hub although '
                                           'creating it locally using Dockerfile.')
    docker_report_parser.add_argument('-dh', '--dockerhost', action='append',
                                      help='Informs IP or docker host name address to docker client host machine. '
                                           'Default: localhost.')
    docker_report_parser.add_argument('-nd', '--nodocker', action='store_true', help='Docker execution ignored.')
    docker_report_parser.set_defaults(handler=rep.docker_report)

    ''' Report Clear parser '''
    report_clear_parser = subparsers.add_parser('clear', help='Limpar arquivos e diretórios de relatório.')
    report_clear_parser.set_defaults(handler=rep.clear)

    ''' Run parser'''
    run_parser = subparsers.add_parser('run', help='Executa o projeto FTSA.')
    run_parser.add_argument('-p', '--parallel', help='Número de instâncias paralelas. Ex: 2 (duas) etc.')
    run_parser.add_argument('-i', '--include', action='append',
                            help='Informa as tags que devem ser incluídas. Ex: all')
    run_parser.add_argument('-e', '--exclude', action='append',
                            help='Informa as tags que devem ser excluídas. Ex: fe')
    run_parser.set_defaults(handler=rep.run)

    ''' Init parser '''
    init_parser = subparsers.add_parser('init', help='Inicializa um projeto FTSA (TJPB, básico, com login).')
    init_parser.add_argument('project_name', help='Informa o NOME do projeto FTSA.')
    init_parser.add_argument('-e', '--example', action='store_true',
                             help='Cria um projeto para o FTSA-TJPB (com exemplo).')
    init_parser.add_argument('-s', '--services', action='store_true',
                             help='Cria um projeto para o FTSA-Services (testes REST / API ou XML).')
    init_parser.set_defaults(handler=ini.init)

    ''' Execute command with args '''
    args = parser.parse_args()
    args.handler(args)

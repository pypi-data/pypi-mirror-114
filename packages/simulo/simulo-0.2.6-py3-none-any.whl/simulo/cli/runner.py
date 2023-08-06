#https://www.youtube.com/watch?v=kNke39OZ2k0

import click
from simulo.upload import data_upload
from simulo.auth import authenticator
from os import listdir
from os import environ
from os.path import isfile, join

def execute_upload(username: str, password: str, img_path: str, img_type: str):
    auth = authenticator.Authenticate()
    auth_info = auth.login(username, password)
    # print(auth_info.__dict__)
    dicom_img_path = img_path
    du = data_upload.DataUploadClient()
    files = [join(dicom_img_path, f) for f in listdir(dicom_img_path) if isfile(join(dicom_img_path, f))]
    list_of_lists = []
    list_of_lists.append(files)
    response = du.create_session(list_of_lists, img_type, auth_info)
    session_id = response['session_id']
    if (response['status_code'] == 201):
        # assert du.to_string() == "My session id is {0}.".format(session_id)
        print('session created')
        response = du.start_session(session_id, auth_info)
        if (response['status_code'] == 200):
            print('started session')
            response = du.send_files(session_id, auth_info)
            if (response == True):
                print('Finished sending file chunks')
                response = du.end_session(session_id, auth_info)
                if (response['status_code'] == 200):
                    print('ended session')

class Config(object):
    def __init__(self):
        self.verbose = False
pass_config = click.make_pass_decorator(Config, ensure=True)

class HiddenPassword(object):
    def __init__(self, password=''):
        self.password = password
    def __str__(self):
        return '*' * len(self.password)

@click.group()
@click.option('--verbose', is_flag=True)
@click.option('--username', help='Your username', type=click.STRING, required=True)
#@click.option('--password', help='Your password', type=click.STRING, required=True)
@click.option('--password',
              prompt=True,
              default=lambda: HiddenPassword(environ.get('PASSWORD', '')),
              hide_input=True)
@pass_config
def cli(config, verbose, username, password):
    config.verbose = verbose
    config.username = username
    config.password = password

@cli.command()
@click.option('--file-type', type=click.Choice(['DICOM', 'NIFTI']), help='The type of files that you want to upload', required=True)
@click.argument('upload-path', type=click.Path(), default='.', required=True)
@pass_config
def upload(config, file_type, upload_path):
    """This command lets you upload all the files in a given directory"""
    if config.verbose:
        click.echo('we are in verbose mode')
        click.echo('command is upload')
        click.echo('username is %s' % config.username)
        #click.echo('password is %s' % config.password)
        click.echo('file types is %s' % file_type)
        click.echo('upload path is %s' % upload_path)
    click.echo('about to upload...')
    execute_upload(config.username, config.password, upload_path, file_type)


def main():
    cli()

if __name__ == "__main__":
  main()

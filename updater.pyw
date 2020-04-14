from urllib import request
import json, tarfile, os, io, platform, sys, subprocess

dname = os.path.dirname(os.path.abspath(__file__))
os.chdir(dname)

if (os.path.basename(dname) != 'Topological-Navigation-Editor') and (os.path.basename(dname) != 'pkgs'):
    if not os.path.isdir('Topological-Navigation-Editor'):
        os.mkdir('Topological-Navigation-Editor')
    os.chdir('Topological-Navigation-Editor')
    dname = os.getcwd()

query_address = 'https://github.com/Matthew-J-Bennett/Topological-Navigation-Editor/releases/latest'
query_info = json.loads(request.urlopen(query_address).read().decode('utf-8'))

tarball_url = query_info['tarball_url']
version = query_info['tag_name']

tarball_contents = request.urlopen(tarball_url).read()
tarball = io.BytesIO(tarball_contents)

with tarfile.open(fileobj=tarball) as tar:
    for each in tar:
        new_name = each.name.split('/')
        new_name.pop(0)
        new_name = '/'.join(new_name)
        if new_name != '':
            contents = tar.extractfile(each)
            if os.path.isfile(new_name):
                os.remove(new_name)
            with open(new_name, 'wb') as file:
                file.write(contents.read())
    with open('.version', 'w') as file:
        file.write(version)

if platform.system() == 'Windows' or platform.system() == 'Darwin':
    addr = dname + '/Topological-Navigation-Editor.pyw'
    subprocess.Popen(['', addr], executable=sys.executable)
else:
    print(platform.system)

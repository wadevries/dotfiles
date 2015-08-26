#!/usr/bin/env python
import glob
import os
import shutil

HOME = os.getenv('HOME')


def confirm(question, choices, default):
    def ask_question():
        return raw_input("{}? [{}] ".format(question, default))

    response = ask_question()
    while response not in choices or response == '':
        response = ask_question()

    response = response or default
    return response


def install_symlinks():
    symlinks = glob.glob('../**/*.symlink')
    for link in symlinks:
        link_base = os.path.splitext(os.path.basename(link))[0]
        src = os.path.abspath(link)
        
        destination = os.path.join(HOME, '.{}'.format(link_base))
        
        if os.path.exists(destination):
            if not (os.path.islink(destination) and os.readlink(destination) == src):
                choice = confirm(
                    'Destination {} exists, (O)verwrite,  (B)ackup, or (S)kip'.format(destination), 'obs', 'o')

                if choice == 's':
                    continue
                if choice == 'b':
                    shutil.move(destination, "{}.bak".format(destination))
                if choice == 'o':
                    os.unlink(destination)

            elif os.path.islink(destination):
                print "Link to {} exists, skipping".format(src)
                continue

        os.symlink(src, destination)


if __name__ == '__main__':
    install_symlinks()

# coding=utf-8

"""
Simple FTP Tool
"""

import ftplib
import os
import argparse


def ftp_upload(address, username, password, target, dstpath):
    """
    Command for uploading file via ftp to server
    """
    session = ftplib.FTP(host=address)
    try:
        login_response = session.login(user=username, passwd=password)

        if "230" in login_response:
            print("Login successful...")
            print("\n")

            # Change to destination path
            if session.pwd() != dstpath:
                session.cwd(dstpath)

            print("Upload path: " + session.pwd())

            if os.path.isfile(target):
                if not target.startswith('.'):
                    file = open(target, 'rb')  # file to send
                    file_name = target.split('/')[-1]

                    print("Uploading file: {}".format(target))

                    session.storbinary("stor {}".format(file_name), file)  # send the file
                    file.close()  # close file and FTP

                print("\nUpload complete...")
            else:
                for i in os.listdir(target):
                    path = os.path.join(target, i)

                    if not i.startswith('.') and os.path.exists(path):
                        print("Uploading file: ".format(str(i)))

                        file = open(path, 'rb')  # file to send
                        session.storbinary("stor {}".format(i), file)  # send the file
                        file.close()  # close file and FTP

                print("\nUploading complete...")
    except Exception as e:
        print(e)
    finally:
        session.quit()


def ftp_download(address, username, password, target, dstpath):
    """
    Command for downloading file via ftp to server
    """
    session = ftplib.FTP(host=address)
    try:
        login_response = session.login(user=username, passwd=password)

        # Login confirmation
        if not "230" in login_response:
            print("Login failure...")
            return

        # Path correction
        if dstpath[-1] != "/":
            dstpath += "/"

        print("Login successful...")
        print("Downloading target: {}".format(target))

        filename = target.split("/")[-1]
        filepath = target.replace(filename, "")
        session.cwd(filepath)
        session.retrbinary("RETR {}".format(filename), open(dstpath + filename, 'wb').write)
        print("Download complete...")

    except Exception as e:
        print("Error occurred...")
        print(e)
    finally:
        session.quit()


if __name__ == "__main__":
    ACTIONS = {"upload": ['upload', 'UPLOAD', 'u'], "download": ['download', 'UPLOAD', 'u']}
    args = argparse.ArgumentParser(description="Simple FTP Tool")
    args.add_argument('--action', '-n', choices=ACTIONS["upload"] + ACTIONS["download"],
                      type=str, metavar='', help="action to be performed")
    args.add_argument('--host', '-a', type=str, metavar='', help="host address")
    args.add_argument('--username', '-u', type=str, metavar='', help="user account on host")
    args.add_argument('--password', '-p', type=str, metavar='', help="user password")
    args.add_argument('--target', '-t', type=str, metavar='', help="file or dir to be uploaded/downloaded")
    args.add_argument('--destination', '-d', type=str, metavar='', help="destination to send/retrieve target")
    args = args.parse_args()

    if args.action in ACTIONS['upload']:
        ftp_upload(address=args.host,
                   username=args.username,
                   password=args.password,
                   target=args.target,
                   dstpath=args.destination)

    elif args.action in ACTIONS["download"]:
        ftp_download(address=args.host,
                     username=args.username,
                     password=args.password,
                     target=args.target,
                     dstpath=args.destination)

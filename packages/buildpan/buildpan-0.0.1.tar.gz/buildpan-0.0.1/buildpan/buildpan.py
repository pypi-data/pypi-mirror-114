
"""
    Title: buildpan
    Module Name: buildpan
    Author: Akash Dwivedi
    Language: Python
    Date Created: 26-07-2021
    Date Modified: 29-07-2021
    Description:
        ###############################################################
        ##  Main operating file for all the cli commands             ## 
         ###############################################################
 """
import git
import os
import click
import git
import sys
from github import Github


from commands import auth
from commands import selectrepo
from commands import allrepo
# from commands import reset
from commands import webhook


@click.group(help="CLI tool to manage full development cycle of projects")
def buildpan():
    pass


@buildpan.command()
# @click.option('--token', '-e', default="dev", prompt='Enter token ', help='Token for authentiication')
def print():
    """Authenticate your self"""
    print(auth.tk2)

buildpan.add_command(auth.auth)
buildpan.add_command(allrepo.allrepo)
buildpan.add_command(selectrepo.selectrepo)
# buildpan.add_command(reset.reset)
buildpan.add_command(webhook.create_webhook)
if __name__ == '__main__':
    buildpan()
    



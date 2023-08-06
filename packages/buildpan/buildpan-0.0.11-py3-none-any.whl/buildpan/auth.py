
"""
    Title: auth.py
    Module Name: auth.py
    Author: Akash Dwivedi
    Language: Python
    Date Created: 26-07-2021
    Date Modified: 29-07-2021
    Description:
        ###############################################################
        ## Authenticate the user account    ## 
         ###############################################################
 """
import git
import os
import click
import git
import sys
from github import Github


@click.command()
@click.option('--token', '-e', default="dev", prompt='Enter token ', help='Token for authentiication')
def auth(token):
    """Authenticate your self"""
    token="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"
    
    tk1=token
    g=Github(token)
    click.echo(f"Your Token is  {g}!")
    click.echo(f"Your Token is  {token}!")
    repo(tk1)
    

def repo(tk1):
   tk2=tk1
   g=Github(str(tk1))
   print(g)
   i=1
   for repo in g.get_user().get_repos():
    print(i," ",repo.name)
    i=i+1
   

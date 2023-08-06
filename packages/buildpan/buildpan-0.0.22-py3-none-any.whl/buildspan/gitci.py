
"""
    Title: buildpancd
    Module Name: buildpan
    Author: Akash Dwivedi
    Language: Python
    Date Created: 26-07-2021
    Date Modified: 28-07-2021
    Description:
        ###############################################################
        ##  Authenticate and performs github operations 
        ###############################################################
"""
import os
import click
import sys
import git
import subprocess
from github import Github


def main():
    buildpan()
@click.group()
@click.pass_context
def buildpan(self):
    pass
@buildpan.command()
@click.option('--token', '-e', default="dev", prompt='Enter token ', help='Token for authentiication')
def auth(token):
    """Authenticate your self"""
    """
    param : token is the argument which is a aceess token for getting access to the
    github repository.
    Variables Used:
    token : Stores the github access token 
     
    return: Nil
    """
    global tk1
    tk1=token
    g=Github(token)
    click.echo(f"Your Token is  {g}!")
    click.echo(f"Your Token is  {token}!")
    repo(tk1)
    

def repo(tk1):
   tk2=tk1
   g=Github(str(tk1))
   print(g)
   for repo in g.get_user().get_repos():
    print(repo.name)

    

@buildpan.command()
@click.option('--token', '-e', default="dev", prompt='Enter token ', help='Shows all the repo in the account')
@click.option('--username', '-e', default="dev", prompt='Enter username ', help='Enter the github username')
def selectrepo(token,username):
    '''Select the repo in the account '''
    """
    param : token is the argument which is a aceess token for getting access to the
    github repository.
    Variables Used:
    token : Stores the github access token 
    repo : stores the reposirory 
    content: Stores the files avaialable in the files in the repository
    return: Nil
    """
    g=Github(token)
    print(g)
    i=1
    for repo in g.get_user().get_repos():
     print(i," ",repo.name)
    i=i+1
    name=input("Enter the repo name")
    repo=g.get_repo(username+"/"+name)
    reponame=username+"/"+name
    print(reponame)
    content=repo.get_contents("")
    for file in content:
       print("FILE NAME ARE ",file)
   


@buildpan.command()
@click.option('--token', '-e', default="dev", prompt='Enter token ', help='Shows all the repo in the account')
def allrepo(token):
    '''Shows all the repo in the account '''
    """
    param : token is the argument which is a aceess token for getting access to the
    Variables Used:
         g : Stores the value of objest of the github.
         repo : Stores the value of the name of the repository 
         repo.name:displays the name of the repository fetched from the github 
     return : Nil

    """
    print('Choose the repo type ')
    g=Github(token)
    print(g)
    for repo in g.get_user().get_repos():
     print(repo.name)

@buildpan.command()
@click.option('--token', '-e', default="dev", prompt='Enter token ', help='Create Repo')
def crepo(token):
    '''Create repo in your github '''
    """
    param : token is the argument which is a aceess token for getting access to the
    Variables Used:
         g : Stores the value of objest of the github.
         Crepo : Stores the value of the name of the repository from the user
         visability : Stores the type of the visability
         repo1:Stores the current instance of the newly built repository
     return : Nil

    """
    g=Github(token)
    user=g.get_user()
    click.echo(f"Enter the name of your repository")
    Crepo=input()
    click.echo(f"Do you want to make it private? Y/N")
    visability=input()
    if(visability=='y'or 'Y'):
        repo1=user.create_repo(Crepo,private=True)
    else:
        repo1=user.create_repo(Crepo)
    click.echo(f"Repository created")



    


cli = click.CommandCollection(sources=[buildpan])

 
if __name__ == '__main__':
    main()
    buildpan()
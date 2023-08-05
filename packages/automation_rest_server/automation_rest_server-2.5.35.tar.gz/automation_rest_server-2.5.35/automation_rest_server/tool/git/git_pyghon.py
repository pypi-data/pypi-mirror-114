import git

with git.Repo.init(path=r'D:\Dell\test-platform') as repo:
    if repo.is_dirty() is True:
        repo.index.checkout(force=True)
    remote = repo.remote()
    remote.pull()
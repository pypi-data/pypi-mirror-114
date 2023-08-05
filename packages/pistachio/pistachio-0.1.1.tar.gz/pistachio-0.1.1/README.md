# pistachio
Pistachio aims to simplify reoccurring tasks when working with the file system.

## Developing

To install pistachio, along with the tools you need to develop and run tests, run the following in your virtualenv:

```bash
$ pip install -e .[dev]
```

## Install

You can install pistachio by running the following command.

```bash
$ pip install pistachio
```

## Usage

To use pistachio you can inport the module by running the following commands.

```python
>>> import pistachio
```

### Describe

Method to return a description for the resource.

```python
>>> print(json.dumps(pistachio.describe("README.md"), sort_keys=2, indent=2))
{
  "exists": true,
  "is_directory": false,
  "is_file": true,
  "is_symlink": false,
  "name": "README.md",
  "path": "README.md"
}
```

print(json.dumps(pistachio.tree("src"), sort_keys=2, indent=2))

### Exists

You can confirm if a directory, file or symbolic link exists using the following method.

```python
>>> pistachio.exists("README.md")
True
```

### Get MD5 Hash

This method will return the MD5 hash string for a specific file.

```python
>>> pistachio.get_md5_hash("README.md")
"2f853812babf98322618edeb24359591"
```

### Is Directory

Is the resource a directory? True or False.

```python
>>> pistachio.is_directory("README.md")
False
```

### Is File

Is the resource a file? True or False.

```python
>>> pistachio.is_file("README.md")
True
```

### Is Symlink

Is the resource a symbolic link? True or False.

```python
>>> pistachio.is_symlink("README.md")
False
```

### Touch

This method will create an empty file with a given filename and directory path.

```python
>>> pistachio.touch("foo.bar")
True
```

### Tree

This method will return a list of directories, files and symlinks below a specific directory.

```python
>>> print(json.dumps(pistachio.tree("src"), sort_keys=2, indent=2))
{
  "path": "src",
  "results": [
    {
      "exists": true,
      "is_directory": false,
      "is_file": true,
      "is_symlink": false,
      "name": "__init__.py",
      "path": "./__init__.py"
    },
    {
      "exists": true,
      "is_directory": false,
      "is_file": true,
      "is_symlink": false,
      "name": "pistachio.py",
      "path": "./pistachio.py"
    }
  ]
}
```

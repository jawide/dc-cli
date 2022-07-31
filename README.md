Docker compose software cli

## Usage

install package

```bash
dc install package_name
```

uninstall package

```bash
dc uninstall package_name
```

update package

```bash
dc update package_name
```

### Test Publish

```bash
rm -rf dist & python -m build && python -m twine upload --repository testpypi dist/*
```

```cmd
rd /S /Q dist & python -m build && python -m twine upload --repository testpypi dist/*
```

```bash
pip uninstall -y dc-cli-jawide && pip install --index-url https://test.pypi.org/simple/ --no-deps --no-cache-dir --upgrade dc-cli-jawide
```

### Publish

```bash
rm -rf dist & python -m build && python -m twine upload dist/*
```

```cmd
rd /S /Q dist & python -m build && python -m twine upload dist/*
```

```bash
pip uninstall -y dc-cli-jawide && pip install --no-cache-dir --upgrade dc-cli-jawide
```

### Future

- [ ] 修改install子命令使其只下载应用不启动应用，添加更多命令，例如stop、start、pause
- [ ] 添加search子命令，提供应用搜索功能
- [ ] 添加ps子命令，提供应用运行状态显示功能
- [ ] 添加config子命令，用于配置全局变量
- [ ] 优化错误信息的提示
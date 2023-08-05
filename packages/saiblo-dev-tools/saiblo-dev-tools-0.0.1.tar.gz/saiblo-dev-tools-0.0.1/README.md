# 游戏开发人员脚本工具



## 配置

安装本工具：

```shell
pip3 install saiblo-dev-tools
```

使用前请先执行：

```shell
saiblo-dev-tools init
```

脚本会在 ~/ 下创建 .saiblo-dev-tools 目录，里面将会存放所有配置文件。初始化后，请编辑 ~/.saiblo-dev-tools/config.json，按照模板填写配置文件。



## 选项

脚本包含了若干子命令，在每个子命令下有对应的帮助信息：

```shell
saiblo-dev-tools <subcommand> --help
```

### init

```shell
saiblo-dev-tools init
```

会将 ~/.saiblo-dev-tools/config.json 和 database.json 复原为模板文件。

### ai

AI 管理脚本。AI 以 `<tag>: <token>` 的形式存储在 ~/.saiblo-dev-tools/database.json 的 `ai` 字段下。`<tag>` 为人类友好的名称，`<token>` 用于在 Saiblo 数据库中唯一确定某个 AI. `"human"` 保留给人类玩家，请勿使用。

- ```shell
  -d, --delete <tag>
  ```

  删除名为 `<tag>` 的 AI，并将其 token 打印出来，防止误操作。

- ```shell
  -i, --insert <tag> <token>
  ```

  添加 AI，若 `<tag>` 已存在，则会覆盖，但会将原有 AI 的 token 打印出来。脚本**不会**对 token 的合法性进行检验。

- ```shell
  -l, --list
  ```

  显示数据库中所有 AI.

- ```shell
  -r, --rename <old_tag> <new_tag>
  ```

  将名为 `<old_tag>` 的 AI 更名为 `<new_tag>`. 若 `<new_tag>` 已存在，则会覆盖，但会将原有 AI 的 token 打印出来。

- ```shell
  -u, --upload <config_path>
  ```

  上传 AI 至 Saiblo，并将 token 添加进本地数据库。`<config_path>` 为配置文件的路径，格式如下：

  ```jsonc
  {
      "game": number,  // <game_id>
      "language": string,  // {c, cmake, cpp, make, python, python_zip}
      "path": string,  // AI 代码的路径，需要打包成单文件
      "tag": string,  // <tag>
  }
  ```

### game

游戏管理脚本。

- ```shell
  -t, --test <config_path> <result_dir>
  ```

  在 Saiblo 上发起一次评测。`<result_dir>` 为存放评测信息的目录，将包含配置信息、评测结果、回放文件。`<config_path>` 是配置文件的路径，格式如下：

  ```jsonc
  {
      "ai": [
          string,  // <tag>
          ...
      ],
      "config": any,  // 自定义配置信息，若无，可以填空字符串
      "game": number,  // <game_id>
  }
  ```

  saiblo-dev-tools 现已支持启动人机、人人对战，你只需要将上述配置文件中原本填写 ai tag 的位置改为填写 `"human"`，即可在相应位置添加人类玩家。该脚本随后会输出人类玩家的 token.

- ```shell
  -u, --upload <config_path>
  ```

  上传游戏逻辑至 Saiblo. `<config_path>` 为配置文件的路径，格式如下：

  ```jsonc
  {
      "id": number,  // <game_id>
      "path": string,  // 游戏逻辑的路径，需要打包成单文件
  }
  ```
  
  **注意**：目前 Saiblo 对游戏逻辑代码的管理与 AI 不同，因此该命令会覆盖 Saiblo 上先前的游戏逻辑，请谨慎使用。

### login

```shell
saiblo-dev-tools login <username>
```

登录 Saiblo 开发账号。脚本将会在 ~/.saiblo-dev-tools/cookie 中保存登录凭据，请妥善保管。

### logout

```shell
saiblo-dev-tools logout
```

删除 ~/.saiblo-dev-tools/cookie，下次使用与 Saiblo 交互的命令将需要登录。


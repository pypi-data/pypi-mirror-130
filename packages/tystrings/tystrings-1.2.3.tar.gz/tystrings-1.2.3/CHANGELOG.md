1.2.2
---
#### Feature
1. Support python 3

1.2.0
---
#### Feature
1. `translate` subcommand add `--appid` and `--secret`

#### Bug Fixed
1. Translate Error

1.1.2
---
#### Bug Fixed
1. diff table Output Error

  ```
  +----+---------+---------+-------------+---------+
  |    |   File1 | File2   | Key         | Value   |
  |----+---------+---------+-------------+---------|
  | +  |       2 |         | diff.test.0 | Test0   |
  | -  |       2 |         | diff.test.0 | Test    |
  +----+---------+---------+-------------+---------+
  ```

  should be

  ```
  +----+---------+---------+-------------+---------+
  |    |   File1 | File2   | Key         | Value   |
  |----+---------+---------+-------------+---------|
  | +  |       2 |         | diff.test.0 | Test0   |
  | -  |         |       2 | diff.test.0 | Test    |
  +----+---------+---------+-------------+---------+
  ```

1.1.1
---
#### Bug Fixed
1. Baidu Translator Encode Error
2. Translator Incremental Updates Error

1.1.0
---
#### Feature
1. add `lint` subcommand

  Validates a `.strings` file.
2. add `diff` subcommand

  Compare `.strings` files line by line.

#### Bug Fixed
1. Parser Error [issue #1](https://github.com/luckytianyiyan/TyStrings/issues/1)
    ```
    /* No comment provided by engineer. */
    "parsing.test.4"  ="Test4
    Test4
    Test4Test4Test4
    Test4
    ";
    ```

1.0.1
---
#### Feature
1. add `translate` subcommand
#### Enhancement
1. support multiple destination
  ```
  -o DESTINATIONS [DESTINATIONS ...]
  ```
2. tystrings as subcommand 'tystrings generate'

0.2.0
---
1. fixed cli crash when encoding is not `UTF-16`
2. fixed generate strings error.
  － The first line of the file is not processed.
  － The lines that are in the format of chaos is not processed.
3. cli add `--utf8` option
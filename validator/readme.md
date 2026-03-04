# Запуск валидатора ассетов

## Валидные ассеты
```
> python assetinfo_validator.py ./test_pass.json
PASS
```

## Невалидные ассеты
```
> python assetinfo_validator.py ./test_fail.json
Errors:
Asset `Stone`: VertexCount 1000000 > 10000
Asset `Stone`: TriangleCount 2500000 > 5000
Asset `T_Stone_Normal`: Texture size 9998x3568 is not powers of two
Asset `T_Stone_Normal`: Texture file size 16.00 MB > 2MB
Warnings:
Asset `Stone`: MaterialsCount 8 > 3
Asset `Stone`: Name `Stone` not starts with `SK_` or `SM_`
Asset `T_Stone_Normal`: Texture aspect 9998:3568 is not 1:1 or 1:2 or 2:1
Asset `T_Stone_Roughness`: Texture aspect 16:1024 is not 1:1 or 1:2 or 2:1
FAIL
```
# Threading-util

#### Консольная утилита для многопоточного копирования или перемещения файлов
- Пример запуска утилиты:

python util.py --operation move --from /home/user/projects --to /root/

python util.py --operation copy --from /home/user/projects --to /root/

Есть возможность указать количество одновременно копируемых/переносимых файлов это значение должно браться из параметра threads

- Пример запуска утилиты:

python util.py --operation copy --from /home/user/projects/*.md --to /root/  --threads 10

echo "Drop database"
yes | python cli.py drop-db
echo "Reinit DB"
python cli.py init-db
echo "Read texts"
python cli.py read-plain-text -n 20NG 20ng.txt
echo "Init project"
python cli.py init-project project_config.json

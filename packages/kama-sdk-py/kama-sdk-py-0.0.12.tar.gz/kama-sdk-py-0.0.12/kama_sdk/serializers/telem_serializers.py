from typing import Dict


def ser_config_backup_record(record: Dict) -> Dict:
  config: Dict = record.get('config', {})

  return dict(
    id=str(record.get('_id')),
    space=record.get('space'),
    name=record.get('name'),
    trigger=record.get('trigger'),
    status=config.get('status'),
    ktea=config.get('ktea', {}),
    kama=config.get('kama', {}),
    timestamp=record.get('timestamp')
  )


def ser_config_backup_full(record: Dict) -> Dict:
  return dict(
    **ser_config_backup_record(record),
    config=record.get('config', {})
  )

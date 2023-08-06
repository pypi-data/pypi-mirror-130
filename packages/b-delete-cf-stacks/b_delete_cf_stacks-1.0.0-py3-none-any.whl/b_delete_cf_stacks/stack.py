from typing import Dict, Any


class Stack:
    def __init__(self, stack_summary: Dict[str, Any]) -> None:
        self.__stack_id = stack_summary['StackId']
        self.__stack_name = stack_summary['StackName']
        self.__stack_status = stack_summary['StackStatus']

    @property
    def stack_id(self) -> str:
        return self.__stack_id

    @property
    def stack_name(self) -> str:
        return self.__stack_name

    @property
    def stack_status(self) -> str:
        return self.__stack_status

    def __str__(self) -> str:
        return f'{self.__stack_name:25} [{self.__stack_status}]'

# Robotframework-excelutil library

This Robotframework Excel Util library provides Robot keywords to Open, Read, Write and Save XLSX files. 
This library uses python to read and write datas in xlsx files.

## Pre-requisities
- Python - 3.x (Not tested with Python 2.x)
- Robotframework - 4.x (Not tested with other versions)
- Openpyxl

## Installation
```pip install robotframework-excelutil```

## Settings
| Library    ExcelUtil |

## To open Excel
| Open Excel |  C:\\Data\\ExcelTest.xlsx  |

## To get sheetnames of the workbook
- | Open Excel |  C:\\Data\\ExcelTest.xlsx  |
- | Get sheet names      |

## To get column count of the given sheet
- | Open Excel |  C:\\Data\\ExcelTest.xlsx  |
- | Get Column count     |  Sheet1 |

## To get Row count of the given sheet
- | Open Excel |  C:\\Data\\ExcelTest.xlsx  |
- | Get Row count     |  Sheet1 |

## To get the value of a cell by giving the sheetname, row value & column value
- | Read Cell Data By Coordinates     |  SheetName | Row Number |  Column Number  |
- | Read Cell Data By Coordinates     |  Sheet1 |  1  |  1  |

## To Write the value to a call using its co-ordinates
- | Write Data By Coordinates    |  SheetName  | Row Number | Column Number |  Data  |
- | Write Data By Coordinates    | Sheet1 | 1 | 1 |  TestData  |

## To Save the excel file after writing the data.
- Update existing file:
-   | Openexcel File       |  C:\\Data\\ExcelTest.xlsx  |
-   | Save Excelfile       |  C:\\Data\\ExcelTest.xlsx  |

## Save in new file:
- | Openexcel File       |  C:\\Data\\ExcelTest.xlsx  |
- | Save Excelfile       |  D:\\Data\\ExcelRobotNewFile.xlsx  |

## To add a new sheet
| Add new sheet        | SheetName

## License

© 2021 Nagesh B Nagaraja Rao

This repository is licensed under the MIT license. See LICENSE for details.
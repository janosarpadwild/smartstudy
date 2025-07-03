from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator

PASSWORD_VALIDATOR = QRegularExpressionValidator(QRegularExpression("[\u0021-\u007E]+")) #all ascii characters except white space
PERMISSION_CODE_VALIDATOR = QRegularExpressionValidator(QRegularExpression("[a-zA-Z0-9]+")) #letters and numbers
EMAIL_VALIDATOR = QRegularExpressionValidator(QRegularExpression("[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}")) #email format
TASK_ANSWER_VALIDATOR = QRegularExpressionValidator(QRegularExpression("[-+]?[0-9]*\\.?[0-9]+")) #double format
NAME_VALIDATOR = QRegularExpressionValidator(QRegularExpression("[ÁÉÍÓÖŐÚÜŰA-Z][a-zA-ZÁÉÍÓÖŐÚÜŰáéíóöőúüű]*(?:[-\'`\\s][ÁÉÍÓÖŐÚÜŰA-Z][a-zA-ZÁÉÍÓÖŐÚÜŰáéíóöőúüű]*)*"))
COURSE_NAME_VALIDATOR = QRegularExpressionValidator(QRegularExpression("[áéíóöőúüűÁÉÍÓÖŐÚÜŰa-zA-Z]+(?:\\s[áéíóöőúüűÁÉÍÓÖŐÚÜŰa-zA-Z]+)*"))
CLASSNAME_VALIDATOR = QRegularExpressionValidator(QRegularExpression("\\d{1,2}\\.[a-zA-ZÁÉÍÓÖŐÚÜŰáéíóöőúüű\\s]+"))
NUMBER_VALIDATOR = QRegularExpressionValidator(QRegularExpression("\\d{1,2}"))
class ParlerPOError(Exception):
    pass

class FieldIDError(ParlerPOError):
    pass

class MasterInstanceLookupError(ParlerPOError):
    def __init__(self, message):
        super().__init__(message)

class ModelNotTranslatableError(ParlerPOError):
    def __init__(self, model):
        self.model = model
        message = "{} is not a TranslatableModel.".format(model)
        super().__init__(message)

class FieldNotTranslatableError(ParlerPOError):
    def __init__(self, field_id):
        self.field_id = field_id
        message = "{} is not a translatable field.".format(field_id)
        super().__init__(message)

class MissingMsgidError(ParlerPOError):
    def __init__(self):
        message = "Missing msgid."
        super().__init__(message)

class InvalidMsgidError(ParlerPOError):
    def __init__(self):
        message = "Provided msgid is different from the base translation."
        super().__init__(message)

class ProtectedTranslationError(ParlerPOError):
    def __init__(self):
        message = "The base translation can not be modified."
        super().__init__(message)

class InvalidContentTypeIDError(ParlerPOError):
    def __init__(self):
        message = "Invalid content type id."
        super().__init__(message)

class ContentTypeDoesNotExistError(ParlerPOError):
    def __init__(self):
        message = "Content type matching id does not exist"
        super().__init__(message)

class InvalidInstanceFieldIDError(ParlerPOError):
    def __init__(self):
        message = "Invalid instance field id."
        super().__init__(message)

class ModelInstanceDoesNotExistError(ParlerPOError):
    def __init__(self):
        message = "Model instance matching id does not exist."
        super().__init__(message)

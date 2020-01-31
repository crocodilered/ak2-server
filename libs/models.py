class BaseModel(object):

    class Meta:
        fields = None           # tuple of simple fields, except id. order_key is special name.
        translations = None     # tuple of translated fields

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')

        # Shortcuts
        self.__fields = self.Meta.fields
        self.__translations = self.Meta.translations if hasattr(self.Meta, 'translations') else []

        for i in self.__fields:
            setattr(self, i, kwargs.get(i))

        for i in self.__translations:
            setattr(self, i, I18nAttr(i, kwargs.get('translations')))

    @classmethod
    def from_raw(cls, record, translations=None):
        """ Alternative constructor from raw data from db. """
        result = None

        if type(record) is tuple and len(record) == len(cls.Meta.fields) + 1:
            params = {'id': record[-1]}

            if hasattr(cls.Meta, 'translations') and translations:
                params['translations'] = translations

            for idx, i in enumerate(cls.Meta.fields):
                params[i] = record[idx]

            result = cls(**params)

        return result

    def to_dict(self, lang=None):
        d = {'id': self.id}

        for i in self.__fields:
            d[i] = getattr(self, i)

        for i in self.__translations:
            d[i] = getattr(self, i).to_dict(lang)

        return d

    def to_raw(self):
        raw = [getattr(self, i) for i in self.__fields]
        raw.append(self.id)
        return tuple(raw)

    @staticmethod
    def get_db_manager():
        raise Exception('Method must be implemented by child.')

    def get_all_translations(self):
        result = []

        for i in self.__translations:
            attr = getattr(self, i)
            for lang in attr.translations:
                result.append((
                    self.id,
                    lang,
                    attr.code,
                    attr.translations[lang],
                ))

        return result


class I18nAttr:
    """
    Свойство модели, имеющее переводы
        code            код поля. title, description и т.д.
        translations    это dict, в котором ключами являются коды языков,
                        а значениями - переводы.
    """
    def __init__(self, code, translations):
        """ translations - list of tuples вида [(code, lang, value)] """
        self.code = code
        self.translations = {}
        if translations:
            for t in translations:
                if t[0] == code:
                    self.translations[t[1]] = t[2]

    def update(self, data):
        if data and type(data) == dict:
            self.translations.update(data)

    def to_dict(self, lang=None):
        if lang is not None:
            if lang in self.translations:
                return {lang: self.translations[lang]}
            else:
                return {}
        else:
            return self.translations

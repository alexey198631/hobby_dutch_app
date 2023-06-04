from translate import Translator
translator= Translator(to_lang="es")
translation = translator.translate("This is a pen.")

print(translation)
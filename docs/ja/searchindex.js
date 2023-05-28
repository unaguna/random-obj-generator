Search.setIndex({"docnames": ["doc.as_command", "doc.construct_factories", "doc.dict_factory", "doc.external_def", "doc.list_factory", "doc.quickstart", "doc.tips", "doc.tips_json", "doc.tips_timeline", "doc.use_factories", "index", "randog", "randog.exceptions", "randog.factory"], "filenames": ["doc.as_command.rst", "doc.construct_factories.rst", "doc.dict_factory.rst", "doc.external_def.rst", "doc.list_factory.rst", "doc.quickstart.rst", "doc.tips.rst", "doc.tips_json.rst", "doc.tips_timeline.rst", "doc.use_factories.rst", "index.rst", "randog.rst", "randog.exceptions.rst", "randog.factory.rst"], "titles": ["\u30b3\u30de\u30f3\u30c9\u3068\u3057\u3066\u5b9f\u884c", "Factory \u306e\u751f\u6210", "Dict factory", "Factory \u306e\u5916\u90e8\u5b9a\u7fa9\u30d5\u30a1\u30a4\u30eb", "List factory", "\u30af\u30a4\u30c3\u30af\u30b9\u30bf\u30fc\u30c8", "Tips (\u4f7f\u3044\u65b9)", "JSON \u3092\u30e9\u30f3\u30c0\u30e0\u306b\u751f\u6210\u3059\u308b", "\u30e9\u30f3\u30c0\u30e0\u306a\u6642\u7cfb\u5217\u30c7\u30fc\u30bf -- \u524d\u306e\u30c7\u30fc\u30bf\u306b\u4f9d\u5b58\u3059\u308b\u30c7\u30fc\u30bf\u751f\u6210", "Factory \u3092\u4f7f\u7528\u3059\u308b", "random-obj-generator", "randog package", "randog.exceptions package", "randog.factory package"], "terms": {"in": [1, 2, 4, 9, 13], "randog": [0, 1, 2, 3, 4, 5, 7, 8, 9, 10], "is": [2, 4, 9, 13], "an": [], "object": [11, 13], "that": 9, "generates": [], "values": [9, 13], "at": [2, 4], "random": [1, 2, 4, 13], "the": [1, 9, 13], "rules": [], "for": [1, 4, 9, 13], "generation": 4, "are": [], "specified": [], "when": [], "created": [], "if": [], "you": [], "do": [], "not": 2, "care": [], "about": [], "conditions": 1, "other": [], "than": [], "can": [], "create": [1, 2, 9], "by": [1, 2, 4, 8, 13], "simply": 1, "supplying": [], "example": [1, 11, 13], "value": [1, 7, 13], "from": [1, 5, 8, 13], "_example": [0, 1, 3, 5, 8, 13], "want": [], "specify": [], "detail": 1, "using": [], "constructor": [], "corresponding": [], ">>": [1, 2, 4, 5, 7, 8, 9, 13], "import": [0, 1, 2, 3, 4, 5, 7, 8, 9, 13], ".factory": [0, 1, 2, 3, 4, 5, 7, 8, 9, 11], "_a": 1, ".from": [0, 1, 2, 3, 4, 5, 8], "(\"": [1, 2, 3], "\")": [1, 2, 3], "generated": [1, 2, 3, 4, 5, 9, 13], ".next": [1, 2, 3, 4, 5, 7, 8, 9, 13], "()": [0, 1, 2, 3, 4, 5, 7, 8, 9, 13], "assert": [1, 2, 3, 4, 5, 9, 13], "isinstance": [1, 2, 3, 4, 5, 9, 13], "(generated": [1, 2, 3, 4, 5, 9, 13], "str": [0, 1, 4, 9, 12, 13], "with": 1, "_b": 1, ".randstr": [1, 2, 4, 7, 9, 13], "(length": [1, 2, 7, 9, 13], "len": [1, 4, 9, 13], "==": [1, 4, 9, 13], "of": [], "following": [], "argument": [], "nonetype": 1, "(there": [], "no": [], "dedicated": [], "function": 1, "but": [], "const": [1, 13], "be": 9, "used": [], "instead": [], ".)": [], "none": [1, 13], "bool": [1, 4, 13], "randbool": [1, 13], "true": [1, 8, 13], "or": [1, 2, 13], "false": [1, 13], "int": [1, 4, 8, 13], "randint": [1, 13], "integer": 1, "float": [1, 11, 13], "randfloat": [1, 13], "randstr": [1, 13], "string": 1, "list": [0, 1, 8, 9, 13], "randlist": [1, 4, 13], "tuple": [1, 13], "(argument": 1, "=tuple": [1, 4], "dict": [1, 5, 8, 13], "randdict": [1, 13], "decimal": [1, 4, 13], ".decimal": 1, "randdecimal": [1, 13], "datetime": [1, 8, 13], ".datetime": 1, "randdatetime": [1, 13], ".date": 1, "randdate": [1, 13], "date": [1, 13], ".time": 1, "randtime": [1, 13], "time": [1, 13], ".timedelta": 1, "randtimedelta": [1, 13], "timedelta": [1, 8, 13], "candidate": [], "use": [1, 13], "_none": [1, 13], "_nullable": 1, ".or": 1, "get": [], "always": [], "returns": [], "several": [], "methods": [], "determine": [], "multiple": [], "make": 4, "it": [], ".e": [], ".,": [], "as": 1, "uses": [], "and": [0, 1], "examples": [1, 13], "so": [], "will": 9, "boolean": [], "(example": 1, "(-": [1, 8], "\"\"": 1, ", true": 1, "))": [1, 4, 7, 8, 9, 13], "range": 1, "):": [1, 8, 9, 13], "..": [1, 2, 4, 8, 9, 13], "creates": [], "which": 0, "chooses": [], "either": [], "each": 0, "result": 13, "chosen": [], ".union": 1, "...": [1, 2, 4, 7, 8, 13], ".randint": [1, 2, 4, 7], ".randbool": [1, 4], "return": 1, "one": 0, "specific": [], "randchoice": [1, 13], ".randchoice": [1, 2, 8], "allow": 1, "\",": [0, 1, 2, 3, 5, 9, 13], "deny": 1, "\"]": [1, 2, 3, 5, 9, 13], "same": 1, "python": [0, 1, 3, 5, 7], ".const": 1, "= \"": 1, "predefined": [], "this": [], "change": [], "post": [1, 7, 8, 13], "_process": [1, 7, 8, 13], "format": [1, 13], ".randdecimal": [1, 4, 7, 13], "_len": [1, 4, 7, 13], "(lambda": [1, 7, 8, 13], "\"$": [1, 13], ":,": [1, 13], "}\"": [1, 13], "'$": [1, 13], "etc": [1, 13], "$\"": [1, 13], "provided": [], "also": 2, "context": 13, "functions": [], "iterators": [], "include": [], "generator": [], "normally": [], "would": [], "think": [], "could": [], "just": [], "iterator": [1, 9, 13], "directly": [], "method": [], "needed": [], "generate": [0, 4, 9], "elements": [], "generating": [], "itertools": 1, "uuid": [0, 1, 3, 5], "define": 1, "class": [1, 11, 13], "mailaddressfactory": 1, "(randog": 1, "[str": 1, "])": [1, 4], "def": [1, 8], "next": [1, 9, 13], "(self": 1, "* \"": 1, "\"@": 1, ".com": 1, "({": [0, 1, 2, 3, 5, 8], "https": 1, ":/": 1, "docs": 1, ".python": 1, ".org": 1, "library": 1, "/itertools": 1, ".html": 1, "#itertools": 1, ".count": 1, "id": [1, 4, 7], "\":": [0, 1, 2, 3, 5, 7, 8], ".uuid": [0, 1, 3, 5], "name": [0, 1, 2, 3, 5, 7], "lambda": 1, "mail": 1, "[\"": [1, 2, 3, 5, 9, 13], "id\"": 1, ", uuid": [1, 5], ", str": [1, 2, 3, 5], "set": [1, 4], "{\"": [1, 8], "\"}": [1, 7], "endswith": 1, "_callable": [1, 13], "_iterator": [1, 8, 13], "finite": [], "once": [], "terminates": [], "cannot": [], "any": [11, 13], "more": [], "randomly": 10, "like": [], "built": [], "two": [], "ways": [], "code": 9, "look": [], "dictitem": [2, 13], ".randdict": [2, 4, 7], "=randog": [2, 4, 7], "sex": 2, "\"m": 2, "age": [0, 2, 3, 5, 7], "=dictitem": 2, "key": [2, 13], "existence": 2, "),": [2, 8], ", int": [2, 5], "passing": [], "factories": 13, "keyword": [], "arguments": [], "to": [0, 1, 4, 9, 13], "element": 0, "possible": [], "randomize": [], "whether": [], "dictionary": [], "above": [], "see": [], "here": [], "how": [], "build": [], "dictitemexample": [2, 11], "smith": 2, "limited": [], "dictionaries": [], "given": [], "output": 0, "similar": [], "its": [], "pass": [], "wrapped": [], "(or": [], "many": [], "cases": [], "because": [], "needs": [], "tailored": [], "application": [], ".randlist": 4, "],": 4, "records": 4, "single": [], "may": 9, "appropriate": [], "iter": [4, 8, 9, 13], "rather": [], "price": [4, 7], "record": 4, "_list": [4, 13], "(factory": [4, 8, 9, 13], ".iter": [4, 8, 9, 13], "-th": [], "longer": [], "number": [], "repeat": [0, 4], "last": [], "el": 4, "_factories": 4, "therefore": [], "typical": [], "where": [], "has": [], "meaning": [], "only": [], "(el": 4, "randomized": [], "sure": 4, "lengths": 4, "(map": 4, "(len": 4, "pieces": [], "attribute": [], "type": [4, 10, 13], "necessary": [], "separate": [], "schema": [], "since": [], "omitting": [], "tuples": [], "equal": [], "types": [], "accept": [], "guaranteed": [], "([": 4, "a\"": 4, "try": [], "these": [], "steps": [], "prepare": [], "newer": [], "install": 5, "pip": 5, "command": [], "follows": [], "factory": [0, 5, 8, 10, 13], "objects": 0, "})": 5, "some": [], "timeline": 8, "data": [], "depends": [], "on": [], "previous": [], "json": [0, 6, 10], "allows": [], "module": 10, "_json": 7, ".dumps": 7, "(value": 7, "case": [], "we": [], "\"name": 7, "wosar": 7, "5ajmwhngj": 7, "such": [], "converted": [], "default": [7, 13], "specifying": [], "=str": 7, "\"id": 7, "were": [], "outputs": [], "beginning": [], "(v": [7, 9, 13], "non": [], "-random": [], "pseudo": [], "-factories": [], "series": [], "(start": 8, "step": 8, "nxt": 8, "start": 8, "while": 8, "yield": 8, "_randomwalk": 8, "_f": 8, "(datetime": 8, "(hours": 8, "location": 8, "hourly": 8, "},": 8, "seen": [], "definition": 3, "increases": [], "exactly": [], "hour": [], "difference": [], "randomwalk": [], "thus": [], "dependent": [], "was": [], "_iterable": 8, ".by": 8, ").": 8, ".isoformat": 8, "{'": 8, "':": 8, "note": 9, "there": 9, "low": 9, "probability": 9, "they": 9, "identical": 9, "usually": [], "way": [], "sugar": [], "-coated": [], "syntax": [], "although": [], "itself": [], "cnt": 9, "_values": 9, "iterable": 9, "disposable": [], "must": [], "regenerated": [], "infinity": [9, 13], "_iter": [9, 13], "terminated": [], "keys": [9, 13], "foo": [9, 13], "bar": [9, 13], "zip": [9, 13], "(keys": [9, 13], ".infinity": [9, 13], "warn": 9, "running": 9, "below": 9, "continue": 9, "indefinitely": 9, "causes": [], "infinite": [], "loop": [], "handle": [], "(random": 10, "package": 10, "helps": [], "quick": [], "installation": [], "minimal": [], "\u751f\u6210": [0, 2, 5, 6, 9, 10, 13], "elemental": [], "nullable": 10, "union": [10, 13], "choice": 10, "constance": [], "processing": [], "custom": [1, 13], "details": [], "individual": [], "tips": 10, "usage": [], "subpackages": 10, "submodules": 10, "\u7d22\u5f15": 10, "\u30e2\u30b8\u30e5\u30fc\u30eb": [7, 10], ".exceptions": 11, "prop": [11, 13], "_exists": [11, 13], "\u30d9\u30fc\u30b9\u30af\u30e9\u30b9": [11, 12, 13], "objs": 11, "sequence": [11, 13], "exception": 12, "factoryconstructionerror": [12, 13], "message": 12, "property": [12, 13], "item": 13, "rule": [], "args": 13, "kwds": 13, "abc": 13, "generic": 13, "serves": [], "\u30b5\u30f3\u30d7\u30eb": 13, "\u623b\u308a\u5024": [9, 13], "size": 13, "times": 0, "(result": 13, "results": 13, "(results": 13, "\u30d1\u30e9\u30e1\u30fc\u30bf": 13, "--": 13, "abstract": 13, "according": [], "assembling": [], "prob": 13, "rnd": 13, "whose": [], "optional": 13, "callable": 13, "modified": [], "mapping": 13, "modify": [], "fromexamplecontext": 13, "path": 13, "_func": 13, "_customfunc": 13, "_is": 13, "_customized": 13, "_stack": 13, "child": 13, "current": 13, "customized": 13, "recursive": 13, "classmethod": 13, "root": 13, "func": 13, "accepted": [], "match": [], "construction": [], "executed": [], "first": [], "new": [], "passed": [], "recommended": [], "receives": [], "*kwargs": 13, "future": [], "updates": [], "process": [], "should": [], "takes": [], "precedence": [], "over": [], "\u4f8b\u5916": 13, "supported": [], "_true": 13, "inconsistent": [], "weights": 13, "choosing": [], "probabilities": [], "chose": [], "length": [4, 13], "minimum": 13, "maximum": 13, "tzinfo": 13, "literal": 13, "fixed": [], "means": [], "specification": [], "fixes": [], "aware": 13, "corrected": [], "otherwise": [], "changed": [], "supportsfloat": 13, "_inf": 13, "nan": 13, "part": [], "positive": [], "negative": [], "items": 13, "_dict": 13, "hashable": 13, "ignored": [], "*items": 13, "._": 13, "base": 13, "[int": 13, "typing": 13, ".callable": 13, "[[": 13, ".iterator": 13, "[~": 13, ".any": 13, "]]": 13, ", ~": 13, ".t": 13, "= <": 13, "'>": 13, ", rnd": 13, ".random": 13, ".sequence": 13, "equals": [], "=list": 13, "positional": [], "charset": 13, "characters": [], "timezone": [], "information": [], "unit": 13, "atomic": [], "\u30e9\u30f3\u30c0\u30e0": [2, 4, 5, 6, 9, 10, 13], "\u30c7\u30fc\u30bf": [6, 10], "\u3059\u308b": [0, 1, 2, 3, 4, 5, 6, 10, 13], "\u30e9\u30a4\u30d6\u30e9\u30ea": 10, "\u3067\u3059": [0, 1, 8, 9, 10, 13], "\u4ee5\u4e0b": [0, 1, 2, 3, 4, 5, 7, 8], "\u624b\u9806": 5, "\u8a66\u3059": 5, "\u3053\u3068": [0, 1, 2, 3, 4, 5, 7, 8, 9, 13], "\u3067\u304d": [0, 1, 2, 3, 4, 5, 7, 8, 9, 13], "\u307e\u3059": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 13], "\u30af\u30a4\u30c3\u30af\u30b9\u30bf\u30fc\u30c8": 10, "\u4ee5\u4e0a": 5, "\u7528\u610f": [1, 5], "\u30b3\u30de\u30f3\u30c9": [3, 4, 5, 7, 10], "\u30a4\u30f3\u30b9\u30c8\u30fc\u30eb": 10, "\u305f\u3044": [0, 1, 4, 5, 8], "\u30aa\u30d6\u30b8\u30a7\u30af\u30c8": [0, 1, 2, 4, 5, 7, 13], "\u95a2\u6570": [0, 1, 5, 7, 13], "\u6e21\u3059": [1, 2, 4, 5], "\u4f5c\u308b": [1, 3, 5, 7, 8, 9], "\u6700\u5c0f": [10, 13], "\u69cb\u6210": 10, "\u5229\u7528": 10, "\u3053\u306e": [0, 1, 2, 3, 4, 5, 7, 8, 9, 13], "\u30ea\u30b9\u30c8": [0, 4, 5, 13], "\u5358\u306a\u308b": [5, 9], "\u6587\u5b57": [5, 8, 13], "\u5217\u7b49": 5, "\u4f7f\u7528": [0, 1, 3, 6, 7, 8, 10, 13], "\u30eb\u30fc\u30eb": [0, 1, 13], "\u6307\u5b9a": [1, 4, 7, 13], "\u305f\u3081": [0, 1, 4, 7], "\u3082\u3057": [1, 4, 8, 13], "\u578b\u4ee5": 1, "\u6761\u4ef6": [1, 13], "\u3053\u3060\u308f\u3089": 1, "\u306a\u3044": [0, 1, 4, 8, 13], "\u3042\u308c": [1, 4], "\u3060\u3051": [1, 4, 13], "\u3082\u3057\u4ed6": [], "\u5834\u5408": [0, 1, 2, 3, 4, 7, 8, 13], "\u5fdc\u3058": [1, 4, 13], "\u30b3\u30f3\u30b9\u30c8\u30e9\u30af\u30bf": 1, "\u304f\u3060": [1, 4, 9], "\u3055\u3044": [1, 4, 9], "\u57fa\u672c": 10, "\u6e21\u3059\u4f8b": [], "\u8a73\u7d30": [0, 10], "\u3078\u306e": 1, "\u5f15\u6570": [0, 1, 2, 4, 13], "\u5c02\u7528": 1, "\u3042\u308a": [0, 1, 4, 9, 13], "\u307e\u305b": [0, 1, 4, 7, 9, 13], "\u4ee3\u308f\u308a": [1, 2, 13], "\u3002)": 1, "\u308c\u308b": [1, 2, 4, 13], "\u3042\u308b": [0, 1, 13], "\u4f5c\u308a": 1, "\u30e1\u30bd\u30c3\u30c9": [1, 8, 9], "\u8fd4\u3059": [1, 13], "\u8907\u6570": [1, 4, 13], "\u3046\u3061": 1, "\u306e\u3044": 1, "\u305a\u308c": 1, "\u3044\u304f\u3064\u304b": 1, "\u65b9\u6cd5": [2, 10], "\u3064\u307e\u308a": 1, "\u5408\u6210": 1, "\u5408\u6210\u578b": 10, "#randog": [], "\u4f8b\u3068\u3057\u3066": [1, 2, 4, 13], "\u3044\u308b": 1, "\u6574\u6570": 1, "\u6587\u5b57\u5217": [0, 1, 13], "\u771f\u507d": 1, "\u5019\u88dc": 1, "\u306a\u308b": [1, 4, 13], "\u305f\u3073": [1, 9], "2\u3064": [1, 2], "\u304b\u3089": [0, 1, 3, 4, 13], "\u9078\u3073": 1, "\u305d\u308c": [1, 3, 13], "\u7d50\u679c": [0, 10, 13], "\u3068\u3057\u3066": [1, 2, 3, 4, 8, 10, 13], "\u8fd4\u3057": [1, 9], "\u540c\u3058\u5024": 1, "`const": [], ">`": [], "\u9078\u629e": 10, "\u5b9a\u6570": 10, "\u306b\u5bfe\u3059\u308b": 1, "\u3042\u3089\u304b\u3058\u3081": [1, 7], "\u5b9a\u7fa9": [0, 1, 8, 10, 13], "\u5909\u66f4": [1, 10, 13], "\u52a0\u5de5": [10, 13], "\u63d0\u4f9b": 1, "\u6587\u8108": 1, "\u305d\u306e": [0, 1, 2, 8, 13], "\u30a4\u30c6\u30ec\u30fc\u30bf": [1, 8, 10, 13], "\u30b8\u30a7\u30cd\u30ec\u30fc\u30bf": [], "\u542b\u3080": 1, "\u30ab\u30b9\u30bf\u30e0": 10, "\u30b8\u30a7\u30cd\u30ec\u30fc\u30bf\u30a4\u30c6\u30ec\u30fc\u30bf": 1, "\u901a\u5e38": [0, 1, 4, 9, 13], "\u308f\u3056\u308f\u3056": 1, "\u3092\u901a\u3055": 1, "\u305a\u3068": 1, "\u307e\u307e": [0, 1, 8, 13], "\u4f7f\u3048": [1, 7], "\u3088\u3044": 1, "\u8981\u7d20": [1, 2, 8, 13], "\u5fc5\u8981": [0, 1, 4, 9], "\u306a\u308a": [1, 2, 4, 8, 9], "\u6709\u9650": 1, "\u4e00\u5ea6": [1, 9], "\u4f7f\u3044": [1, 8, 9], "\u3089\u308c\u308b": 1, "\u306a\u304f": [1, 4, 9], "\u4f5c\u6210": [0, 3, 13], "\u5404\u8981": [2, 4], "\u6bce\u56de": [2, 4], "\u540c\u69d8": [0, 2, 4, 7, 13], "\u3088\u3046": [0, 2, 3, 4, 7, 8, 9, 13], "\u30ad\u30fc\u30ef\u30fc\u30c9": [2, 13], "\u30ad\u30fc": [2, 13], "\u5b58\u5728": [0, 2], "\u304b\u3069\u3046": 2, "\u304b\u3082": [2, 4], "\u4e0a\u8a18": 2, "\u306e\u3088\u3046": [2, 3], ")\u3002": [2, 13], "\u3053\u3061\u3089": 2, "\u8a18\u8f09": [2, 3], ":doc": [], "doc": [], ".construct": [], "\u9650\u3089": 2, "\u51fa\u529b": [2, 10], "\u4e0e\u3048": [2, 4], "\u3089\u308c": [0, 2], "\u3002dict": 2, "\u4e0e\u3048\u308b": 2, "\u4f8b\u304b": 2, "\u3002\u307e\u305f": [2, 8], "\u30e9\u30c3\u30d7": 2, "\u591a\u304f": 4, "\u30b1\u30fc\u30b9": [4, 7, 8], "\u7528\u9014": 4, "\u8abf\u6574": 4, "\u3088\u308a": [4, 13], "`randlist": [], "\u30ec\u30b3\u30fc\u30c9": 4, "\u4f7f\u3046": [4, 7, 8, 9], "\u3079\u304d": [4, 13], "\u3057\u308c": 4, "1\u3064": [0, 4, 8, 13], "\u756a\u76ee": 4, "\u9577\u3044": 4, "\u6700\u5f8c": 4, "\u7e70\u308a\u8fd4\u3057": [4, 10], "\u304c\u3063": 4, "\u3054\u3068": [], "\u7279\u5225": 4, "\u610f\u5473": [4, 13], "\u6301\u305f": 4, "\u5178\u578b": 4, "\u3082\u3057\u9577\u3055": 4, "\u540c\u3058\u9577\u3055": 4, "\u6e21\u3059\u9577\u3055": [], "\u7701\u7565": [0, 3, 4], "\u500b\u6570": 4, "\u500b\u5225": [0, 4], "\u30b9\u30ad\u30fc\u30de": 4, "\u6301\u3064": [4, 8], "\u30a4\u30c6\u30ec\u30fc\u30bf\u30fc": 4, "\u53d7\u3051": [4, 13], "\u5165\u308c\u308b": 4, "\u4fdd\u8a3c": 4, "\u308c\u307e\u305b": 4, "\u4f55\u56de": 9, "\u3067\u3082": [3, 9], "\u7cd6\u8863": 9, "\u69cb\u6587": 9, "\u81ea\u8eab": 9, "\u306a\u306e": 9, "\u4f5c\u308a\u76f4\u3059": 9, "\u5c3d\u304d\u308b": 9, "\u7121\u9650": [9, 13], "\u30eb\u30fc\u30d7": 9, "\u539f\u56e0": 9, "\u53d6\u308a\u6271\u3044": 9, "\u6ce8\u610f": 9, "\u5177\u4f53": 6, "\u7d39\u4ecb": 6, "\u4f7f\u3044\u65b9": 10, "\u6642\u7cfb": [6, 10], "\u4f9d\u5b58": [6, 10], "\u7591\u4f3c": 8, "\u7528\u3044": 8, "\u305f\u3068\u3048\u3070": 8, "\u898b\u3066": 8, "\u308f\u304b\u308b": 8, "\u901a\u308a": [0, 8], "\u306a\u304f\u3061\u3087\u3046\u3069": 8, "\u6642\u9593": 8, "\u305a\u3064": [0, 8], "\u5897\u52a0": 8, "\u3061\u3087\u3046\u3069": 8, "\u30e9\u30f3\u30c0\u30e0\u30a6\u30a9\u30fc\u30af": 8, "\u4e0a\u8ff0": 8, "\u6e21\u3057": 8, "\u5217\u578b": 8, "\u5f62\u5f0f": [7, 10], "\u3067\u304d\u308b": [0, 7], "\u4f8b\u3048": 7, "\u5f97\u3089\u308c": 7, "\u30c7\u30d5\u30a9\u30eb\u30c8": 7, "\u5909\u63db": [0, 7], "\u304a\u3044": 13, "\u5bfe\u5fdc": 13, "\u78ba\u7387": 13, "\u3002for": 13, "\u306a\u3069": 13, "\u76f4\u63a5": [3, 13], "\u3067\u304f": 13, "\u3060\u3055\u3044": [3, 13], "\u56de\u6570": 13, "\u6cbf\u3063": 13, "\u4e71\u6570": 13, "\u30a4\u30f3\u30b9\u30bf\u30f3\u30b9": 13, "\u53d6\u308b": 13, "\u4f3c\u305f\u5024": 13, "\u3082\u3057\u304f": 13, "\u6e21\u3055": 13, "\u307e\u305a": 13, "\u901a\u3055": 13, "\u623b\u308a": 13, "\u30b3\u30f3\u30c6\u30ad\u30b9\u30c8": 13, "\u5c06\u6765": 13, "\u30a2\u30c3\u30d7\u30c7\u30fc\u30c8": 13, "\u5897\u3084": 13, "\u305b\u308b": 13, "\u63a8\u5968": 13, "\u51e6\u7406": 13, "\u5b50\u8981\u7d20": 13, "\u4f7f\u308f": [], "\u3002context": 13, "\u5b9f\u65bd": 13, "\u512a\u5148": 13, "\u4f8b\u3084\u578b": 13, "\u30b5\u30dd\u30fc\u30c8": 13, "\u77db\u76fe": 13, "\u306e\u3046\u3061": 13, "\u9078\u3076": 13, "\u305d\u308c\u305e\u308c": 13, "\u9078\u3070": 13, "\u9577\u3055": 13, "\u4e00\u81f4\u3057": 13, "\u306a\u3051\u308c": 13, "\u306a\u3089": 13, "\u4e00\u3064": 13, "\u6700\u5c0f\u5024": 13, "\u6700\u5927\u5024": 13, "\u304c\u3053\u306e": 13, "\u77ef\u6b63": 13, "\u65e5\u6642": 13, "\u30bf\u30a4\u30e0\u30be\u30fc\u30f3": 13, "\u6642\u523b": 13, "\u6642\u5dee": 13, "\u4ee5\u5916": 13, "\u306e\u307f": 13, "\u5c0f\u6570": 13, "\u90e8\u5206": 13, "\u6841\u6570": 13, "\u5404\u30ad\u30fc": 13, "\u7121\u8996": 13, "\u306a\u304b\u3063": 13, "\u7b49\u3057\u304f": 13, "\u4f4d\u7f6e": 13, "\u60c5\u5831": 13, "\u5358\u4f4d": 13, "\u9078\u3093": 13, "simplest": [], "execute": [], "_definition": 0, "_file": 0, "filename": [], "instance": [], "variable": [], "omitted": [], "print": 0, "options": [], "-repr": 0, "repr": 0, "before": [], "-json": [0, 7], "standard": [], "defined": [], "after": [], "being": [], "strings": [], "_def": [0, 3], ".py": [0, 3], "-output": 0, "option": [], "out": 0, ".txt": 0, "very": [], "practical": [], "thing": [], "done": [], "redirection": [], "feature": [], "shell": [], "exists": [], "combined": [], "described": [], "included": [], "describing": [], "them": [], "-list": [0, 4], "-l": 0, "-repeat": [0, 4], "-r": 0, "repeatedly": [], "contains": 0, "conforms": 0, "hand": [], "separately": [], "different": [], "files": [], "placeholder": [], "txt": 0, "',": 0, "./": [0, 3], "_{": 0, "}.": 0, "placeholders": [], "most": [], "far": [], "loading": [], "runtime": [], "written": [], "bound": [], "save": [], "under": [], "your": [], "load": 3, "_pyfile": [3, 13], "executing": [], "run": [], "external": [], "file": 13, "iteration": [], "pathlike": 13, "io": 13, "\u30d5\u30a1\u30a4\u30eb": [10, 13], "\u30d1\u30b9": 13, "\u3053\u308c": 3, "\u307e\u3067": [3, 13], "\u793a\u3057": 3, "\u307b\u3068\u3093\u3069": 3, "\u5b9f\u884c": [3, 4, 7, 10, 13], "\u307e\u3057": 3, "\u30ed\u30fc\u30c9": 3, "\u5916\u90e8": [0, 10], "\u5909\u6570": [0, 3], "\u30d0\u30a4\u30f3\u30c9": [0, 3], "\u30b3\u30fc\u30c9": 3, "\u3068\u3044\u3046": 3, "\u540d\u79f0": 3, "\u4fdd\u5b58": 3, "\u30d7\u30ed\u30b0\u30e9\u30e0": [0, 3], "\u3082\u3054\u89a7\u304f": 3, "\u7c21\u7d20": 0, "\u30aa\u30d7\u30b7\u30e7\u30f3": [0, 4, 7], "\u6a19\u6e96": 0, "\u5b9a\u3081": 0, "\u30b7\u30a7\u30eb": 0, "\u30ea\u30c0\u30a4\u30ec\u30af\u30c8": 0, "\u6a5f\u80fd": 0, "\u3042\u307e\u308a": 0, "\u5b9f\u7528": 0, "\u7d44\u307f\u5408\u308f\u305b": 0, "\u305d\u308c\u3089": [0, 13], "\u8aac\u660e": 0, "\u4f75\u8a18": 0, "\u7e70\u308a\u8fd4\u3057\u5024": 0, "\u304c\u3042\u308a": 0, "\u307e\u3068\u3081\u3066": 0, "\u4e00\u65b9": 0, "\u3070\u3089": [], "\u5225\u3005": 0, "\u30d7\u30ec\u30fc\u30b9\u30db\u30eb\u30c0\u30fc": 0, "\u3068\u3068\u3082": 0, "\u30d5\u30a9\u30fc\u30de\u30c3\u30c8": 0, "execution": [], ".as": [], "_command": [], "\u307e\u305f": [], "_funcs": 13, "notimplemented": 13, "behaves": [], "until": [], "returned": [], "\u305d\u3082": 13, "\u540c\u3058": 13, "\u52d5\u4f5c": 13, "\u8fd4\u3055": 13, "\u4e00\u9023": 13, "\u305f\u3060\u3057": 13}, "objects": {"": [[11, 0, 0, "-", "randog"]], "randog": [[11, 1, 1, "", "DictItemExample"], [11, 1, 1, "", "Example"], [12, 0, 0, "-", "exceptions"], [13, 0, 0, "-", "factory"]], "randog.DictItemExample": [[11, 2, 1, "", "example"], [11, 2, 1, "", "prop_exists"]], "randog.exceptions": [[12, 3, 1, "", "FactoryConstructionError"]], "randog.exceptions.FactoryConstructionError": [[12, 4, 1, "", "message"]], "randog.factory": [[13, 1, 1, "", "DictItem"], [13, 1, 1, "", "Factory"], [13, 1, 1, "", "FromExampleContext"], [13, 6, 1, "", "by_callable"], [13, 6, 1, "", "by_iterator"], [13, 6, 1, "", "const"], [13, 6, 1, "", "from_example"], [13, 6, 1, "", "from_pyfile"], [13, 6, 1, "", "randbool"], [13, 6, 1, "", "randchoice"], [13, 6, 1, "", "randdate"], [13, 6, 1, "", "randdatetime"], [13, 6, 1, "", "randdecimal"], [13, 6, 1, "", "randdict"], [13, 6, 1, "", "randfloat"], [13, 6, 1, "", "randint"], [13, 6, 1, "", "randlist"], [13, 6, 1, "", "randstr"], [13, 6, 1, "", "randtime"], [13, 6, 1, "", "randtimedelta"], [13, 6, 1, "", "union"]], "randog.factory.DictItem": [[13, 2, 1, "", "factory"], [13, 2, 1, "", "prop_exists"]], "randog.factory.Factory": [[13, 5, 1, "", "infinity_iter"], [13, 5, 1, "", "iter"], [13, 5, 1, "", "next"], [13, 5, 1, "", "or_none"], [13, 5, 1, "", "post_process"]], "randog.factory.FromExampleContext": [[13, 5, 1, "", "child"], [13, 4, 1, "", "current_example"], [13, 4, 1, "", "custom_funcs"], [13, 5, 1, "", "customized"], [13, 4, 1, "", "example_is_customized"], [13, 4, 1, "", "examples"], [13, 5, 1, "", "from_example"], [13, 4, 1, "", "path"], [13, 5, 1, "", "recursive"], [13, 4, 1, "", "rnd"], [13, 5, 1, "", "root"]]}, "objtypes": {"0": "py:module", "1": "py:class", "2": "py:attribute", "3": "py:exception", "4": "py:property", "5": "py:method", "6": "py:function"}, "objnames": {"0": ["py", "module", "Python \u30e2\u30b8\u30e5\u30fc\u30eb"], "1": ["py", "class", "Python \u30af\u30e9\u30b9"], "2": ["py", "attribute", "Python \u306e\u5c5e\u6027"], "3": ["py", "exception", "Python \u4f8b\u5916"], "4": ["py", "property", "Python \u30d7\u30ed\u30d1\u30c6\u30a3"], "5": ["py", "method", "Python \u30e1\u30bd\u30c3\u30c9"], "6": ["py", "function", "Python \u306e\u95a2\u6570"]}, "titleterms": {"factory": [1, 2, 3, 4, 7, 9], "\u751f\u6210": [1, 4, 7, 8], "elemental": [], "types": [], "nullable": 1, "union": 1, "type": 1, "randomly": 1, "choice": 1, "constance": [], "processing": [], "output": [], "custom": [], "details": [], "on": [], "how": [], "to": [], "build": [], "individual": [], "factories": [], "dict": 2, "by": [], "randdict": 2, "from": [2, 4], "_example": [2, 4], "list": 4, "each": [], "elements": [], "length": [], "generate": [], "tuple": 4, "quick": [], "start": [], "installation": [], "minimal": [], "use": [], "tips": 6, "usage": [], "create": [], "json": 7, "decimal": 7, ".t": [], ".c": [], "of": [], "string": [], "random": 10, "timeline": [], "data": [], "depends": [], "previous": [], "change": [], "the": [], "smpl": 8, "_datetime": 8, "str": 8, "as": [], "iterator": [], "-obj": 10, "-generator": 10, "contents": [10, 11], "indices": 10, "and": [10, 11], "tables": 10, "randog": [11, 12, 13], "package": [11, 12, 13], "subpackages": 11, "submodules": 11, "module": 11, ".exceptions": 12, ".factory": 13, "\u30af\u30a4\u30c3\u30af\u30b9\u30bf\u30fc\u30c8": 5, "\u30a4\u30f3\u30b9\u30c8\u30fc\u30eb": 5, "\u6700\u5c0f": 5, "\u69cb\u6210": 5, "\u5229\u7528": 5, "\u57fa\u672c": 1, "\u5408\u6210\u578b": 1, "\u30e9\u30f3\u30c0\u30e0": [1, 7, 8], "\u9078\u629e": 1, "\u5b9a\u6570": 1, "\u7d50\u679c": 1, "\u52a0\u5de5": 1, "\u30ab\u30b9\u30bf\u30e0": 1, "\u8a73\u7d30": 1, "\u65b9\u6cd5": 1, "\u4f7f\u7528": [2, 4, 9], "\u4f5c\u6210": [2, 4], "\u305d\u308c\u305e\u308c": 4, "\u8981\u7d20": 4, "\u9577\u3055": 4, "\u3059\u308b": [7, 8, 9], "\u30a4\u30c6\u30ec\u30fc\u30bf": 9, "\u3068\u3057\u3066": [0, 9], "\u4f7f\u3044\u65b9": 6, "\u6642\u7cfb": 8, "\u30c7\u30fc\u30bf": 8, "\u4f9d\u5b58": 8, "\u5909\u66f4": [0, 8], "\u6587\u5b57\u5217": 7, "run": [], "command": [], "format": [], "file": [], "iteration": [], "external": [], "definition": [], "\u5916\u90e8": 3, "\u5b9a\u7fa9": 3, "\u30d5\u30a1\u30a4\u30eb": [0, 3], "\u30b3\u30de\u30f3\u30c9": 0, "\u5b9f\u884c": 0, "\u51fa\u529b": 0, "\u5f62\u5f0f": 0, "\u7e70\u308a\u8fd4\u3057": 0}, "envversion": {"sphinx.domains.c": 2, "sphinx.domains.changeset": 1, "sphinx.domains.citation": 1, "sphinx.domains.cpp": 8, "sphinx.domains.index": 1, "sphinx.domains.javascript": 2, "sphinx.domains.math": 2, "sphinx.domains.python": 3, "sphinx.domains.rst": 2, "sphinx.domains.std": 2, "sphinx": 57}, "alltitles": {"\u30b3\u30de\u30f3\u30c9\u3068\u3057\u3066\u5b9f\u884c": [[0, "run-as-command"]], "\u51fa\u529b\u5f62\u5f0f\u306e\u5909\u66f4": [[0, "output-format"]], "\u30d5\u30a1\u30a4\u30eb\u51fa\u529b": [[0, "output-to-file"]], "\u7e70\u308a\u8fd4\u3057": [[0, "iteration"]], "Factory \u306e\u751f\u6210": [[1, "construct-factories-generator-of-random-values"]], "\u57fa\u672c\u7684\u306a\u578b": [[1, "elemental-types"]], "Nullable": [[1, "nullable"]], "\u5408\u6210\u578b (Union type)": [[1, "union-type"]], "\u30e9\u30f3\u30c0\u30e0\u306a\u9078\u629e (Randomly choice)": [[1, "randomly-choice"]], "\u5b9a\u6570": [[1, "constance"]], "\u7d50\u679c\u306e\u52a0\u5de5": [[1, "processing-output"]], "\u30ab\u30b9\u30bf\u30e0 Factory": [[1, "custom-factory"]], "\u5404 factory \u306e\u8a73\u7d30\u306a\u751f\u6210\u65b9\u6cd5": [[1, "details-on-how-to-build-individual-factories"]], "Dict factory": [[2, "dict-factory"]], "randdict \u3092\u4f7f\u7528\u3057\u3066\u4f5c\u6210": [[2, "factory-by-randdict"]], "from_example \u3092\u4f7f\u7528\u3057\u3066\u4f5c\u6210": [[2, "factory-by-from-example"], [4, "factory-by-from-example"]], "Factory \u306e\u5916\u90e8\u5b9a\u7fa9\u30d5\u30a1\u30a4\u30eb": [[3, "external-file-definition-of-factory"]], "List factory": [[4, "list-factory"]], "\u305d\u308c\u305e\u308c\u306e\u8981\u7d20\u306e\u751f\u6210": [[4, "each-elements"]], "\u9577\u3055": [[4, "length"]], "tuple \u306e\u751f\u6210": [[4, "generate-tuple"]], "\u30af\u30a4\u30c3\u30af\u30b9\u30bf\u30fc\u30c8": [[5, "quick-start"]], "\u30a4\u30f3\u30b9\u30c8\u30fc\u30eb": [[5, "installation"]], "\u6700\u5c0f\u69cb\u6210\u3067\u306e\u5229\u7528": [[5, "minimal-use"]], "Tips (\u4f7f\u3044\u65b9)": [[6, "tips-usage"]], "JSON \u3092\u30e9\u30f3\u30c0\u30e0\u306b\u751f\u6210\u3059\u308b": [[7, "create-json-randomly"]], "Decimal \u7b49": [[7, "decimal-e-t-c"]], "JSON \u6587\u5b57\u5217\u306e Factory": [[7, "factory-of-json-string"]], "\u30e9\u30f3\u30c0\u30e0\u306a\u6642\u7cfb\u5217\u30c7\u30fc\u30bf -- \u524d\u306e\u30c7\u30fc\u30bf\u306b\u4f9d\u5b58\u3059\u308b\u30c7\u30fc\u30bf\u751f\u6210": [[8, "random-timeline-data-depends-on-previous-data"]], "smpl_datetime \u306e\u578b\u3092 str \u306b\u5909\u66f4\u3059\u308b": [[8, "change-the-type-of-smpl-datetime-to-str"]], "Factory \u3092\u4f7f\u7528\u3059\u308b": [[9, "use-factories"]], "\u30a4\u30c6\u30ec\u30fc\u30bf\u3068\u3057\u3066": [[9, "as-iterator"]], "random-obj-generator": [[10, "random-obj-generator"]], "Contents:": [[10, null]], "Indices and tables": [[10, "indices-and-tables"]], "randog package": [[11, "randog-package"]], "Subpackages and submodules": [[11, "subpackages-and-submodules"]], "Module contents": [[11, "module-randog"]], "randog.exceptions package": [[12, "module-randog.exceptions"]], "randog.factory package": [[13, "module-randog.factory"]]}, "indexentries": {"dictitemexample (randog \u306e\u30af\u30e9\u30b9)": [[11, "randog.DictItemExample"]], "example (randog \u306e\u30af\u30e9\u30b9)": [[11, "randog.Example"]], "example (randog.dictitemexample \u306e\u5c5e\u6027)": [[11, "randog.DictItemExample.example"]], "prop_exists (randog.dictitemexample \u306e\u5c5e\u6027)": [[11, "randog.DictItemExample.prop_exists"]], "randog": [[11, "module-randog"]], "\u30e2\u30b8\u30e5\u30fc\u30eb": [[11, "module-randog"], [12, "module-randog.exceptions"], [13, "module-randog.factory"]], "factoryconstructionerror": [[12, "randog.exceptions.FactoryConstructionError"]], "message (randog.exceptions.factoryconstructionerror \u306e\u30d7\u30ed\u30d1\u30c6\u30a3)": [[12, "randog.exceptions.FactoryConstructionError.message"]], "randog.exceptions": [[12, "module-randog.exceptions"]], "dictitem (randog.factory \u306e\u30af\u30e9\u30b9)": [[13, "randog.factory.DictItem"]], "factory (randog.factory \u306e\u30af\u30e9\u30b9)": [[13, "randog.factory.Factory"]], "fromexamplecontext (randog.factory \u306e\u30af\u30e9\u30b9)": [[13, "randog.factory.FromExampleContext"]], "by_callable() (randog.factory \u30e2\u30b8\u30e5\u30fc\u30eb)": [[13, "randog.factory.by_callable"]], "by_iterator() (randog.factory \u30e2\u30b8\u30e5\u30fc\u30eb)": [[13, "randog.factory.by_iterator"]], "child() (randog.factory.fromexamplecontext \u306e\u30e1\u30bd\u30c3\u30c9)": [[13, "randog.factory.FromExampleContext.child"]], "const() (randog.factory \u30e2\u30b8\u30e5\u30fc\u30eb)": [[13, "randog.factory.const"]], "current_example (randog.factory.fromexamplecontext \u306e\u30d7\u30ed\u30d1\u30c6\u30a3)": [[13, "randog.factory.FromExampleContext.current_example"]], "custom_funcs (randog.factory.fromexamplecontext \u306e\u30d7\u30ed\u30d1\u30c6\u30a3)": [[13, "randog.factory.FromExampleContext.custom_funcs"]], "customized() (randog.factory.fromexamplecontext \u306e\u30e1\u30bd\u30c3\u30c9)": [[13, "randog.factory.FromExampleContext.customized"]], "example_is_customized (randog.factory.fromexamplecontext \u306e\u30d7\u30ed\u30d1\u30c6\u30a3)": [[13, "randog.factory.FromExampleContext.example_is_customized"]], "examples (randog.factory.fromexamplecontext \u306e\u30d7\u30ed\u30d1\u30c6\u30a3)": [[13, "randog.factory.FromExampleContext.examples"]], "factory (randog.factory.dictitem \u306e\u5c5e\u6027)": [[13, "randog.factory.DictItem.factory"]], "from_example() (randog.factory \u30e2\u30b8\u30e5\u30fc\u30eb)": [[13, "randog.factory.from_example"]], "from_example() (randog.factory.fromexamplecontext \u306e\u30e1\u30bd\u30c3\u30c9)": [[13, "randog.factory.FromExampleContext.from_example"]], "from_pyfile() (randog.factory \u30e2\u30b8\u30e5\u30fc\u30eb)": [[13, "randog.factory.from_pyfile"]], "infinity_iter() (randog.factory.factory \u306e\u30e1\u30bd\u30c3\u30c9)": [[13, "randog.factory.Factory.infinity_iter"]], "iter() (randog.factory.factory \u306e\u30e1\u30bd\u30c3\u30c9)": [[13, "randog.factory.Factory.iter"]], "next() (randog.factory.factory \u306e\u30e1\u30bd\u30c3\u30c9)": [[13, "randog.factory.Factory.next"]], "or_none() (randog.factory.factory \u306e\u30e1\u30bd\u30c3\u30c9)": [[13, "randog.factory.Factory.or_none"]], "path (randog.factory.fromexamplecontext \u306e\u30d7\u30ed\u30d1\u30c6\u30a3)": [[13, "randog.factory.FromExampleContext.path"]], "post_process() (randog.factory.factory \u306e\u30e1\u30bd\u30c3\u30c9)": [[13, "randog.factory.Factory.post_process"]], "prop_exists (randog.factory.dictitem \u306e\u5c5e\u6027)": [[13, "randog.factory.DictItem.prop_exists"]], "randbool() (randog.factory \u30e2\u30b8\u30e5\u30fc\u30eb)": [[13, "randog.factory.randbool"]], "randchoice() (randog.factory \u30e2\u30b8\u30e5\u30fc\u30eb)": [[13, "randog.factory.randchoice"]], "randdate() (randog.factory \u30e2\u30b8\u30e5\u30fc\u30eb)": [[13, "randog.factory.randdate"]], "randdatetime() (randog.factory \u30e2\u30b8\u30e5\u30fc\u30eb)": [[13, "randog.factory.randdatetime"]], "randdecimal() (randog.factory \u30e2\u30b8\u30e5\u30fc\u30eb)": [[13, "randog.factory.randdecimal"]], "randdict() (randog.factory \u30e2\u30b8\u30e5\u30fc\u30eb)": [[13, "randog.factory.randdict"]], "randfloat() (randog.factory \u30e2\u30b8\u30e5\u30fc\u30eb)": [[13, "randog.factory.randfloat"]], "randint() (randog.factory \u30e2\u30b8\u30e5\u30fc\u30eb)": [[13, "randog.factory.randint"]], "randlist() (randog.factory \u30e2\u30b8\u30e5\u30fc\u30eb)": [[13, "randog.factory.randlist"]], "randog.factory": [[13, "module-randog.factory"]], "randstr() (randog.factory \u30e2\u30b8\u30e5\u30fc\u30eb)": [[13, "randog.factory.randstr"]], "randtime() (randog.factory \u30e2\u30b8\u30e5\u30fc\u30eb)": [[13, "randog.factory.randtime"]], "randtimedelta() (randog.factory \u30e2\u30b8\u30e5\u30fc\u30eb)": [[13, "randog.factory.randtimedelta"]], "recursive() (randog.factory.fromexamplecontext \u306e\u30e1\u30bd\u30c3\u30c9)": [[13, "randog.factory.FromExampleContext.recursive"]], "rnd (randog.factory.fromexamplecontext \u306e\u30d7\u30ed\u30d1\u30c6\u30a3)": [[13, "randog.factory.FromExampleContext.rnd"]], "root() (randog.factory.fromexamplecontext \u306e\u30af\u30e9\u30b9\u30e1\u30bd\u30c3\u30c9)": [[13, "randog.factory.FromExampleContext.root"]], "union() (randog.factory \u30e2\u30b8\u30e5\u30fc\u30eb)": [[13, "randog.factory.union"]]}})
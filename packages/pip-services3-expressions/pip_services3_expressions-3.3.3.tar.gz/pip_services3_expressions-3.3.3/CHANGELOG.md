# <img src="https://uploads-ssl.webflow.com/5ea5d3315186cf5ec60c3ee4/5edf1c94ce4c859f2b188094_logo.svg" alt="Pip.Services Logo" width="200"> <br/> Tokenizers, parsers and expression calculators in Python Changelog

## <a name="3.3.3"></a> 3.3.3 (2021-07-26)

### Bug fixes
* Fixed sub, mul and div opeartions for AbstractVariantOperations
* Fixed calculation with context

## <a name="3.3.1"></a> 3.3.1 (2021-07-23)

### Features
* Added Type hints
* Rewrite calculation functions without callbacks

### Bug fixes
* Fixed AbstractVariantOperations
* Fixed string conversion

## <a name="3.2.0"></a> 3.2.0 (2021-03-16)

### Features
* Replaced pushback reader with scanner
* Added line and column numbers to errors
* Added escaping strings using tripple brackets '{{{ }}}' according to JSON rules

## <a name="3.1.0"></a> 3.1.0 (2021-03-15)

### Features
* Added Mustache template processing with tokenizers and parsers

## <a name="3.0.0"></a> 3.0.0 (2020-08-01)

### Features
* IO Streaming: IScanner and StringScanner
* Variant (dynamic) values
* Tokenizers (Lexical analyzers)
* Expression calculator
* CSV content processor
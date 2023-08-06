# Шаблонизатор Rocshelf

* template.html
  * [Tag](#template.html | insert)
  * [Inline tag](#template.html | insert)
* template.operators
  * [Insert](#template.operators%20|%20insert)
  * [Insert default](#template.operators%20|%20insert%20or%20default)
  * [If](#template.operators%20|%20if)
  * [Else](#template.operators%20|%20else)
  * [Elif](#template.operators%20|%20elif)
  * [For](#template.operators%20|%20for)
  * [For-else](#template.operators%20|%20for-else)
* template.shelves
  * [Page](#template.shelves%20|%20Shelf-Page)
  * [Wrapper](#template.shelves%20|%20Shelf-Wrapper)
  * [Block](#template.shelves%20|%20Shelf-Block)
  * [Tag](#template.shelves%20|%20Shelf-Tag)
  * [Sub tag](#template.shelves%20|%20Shelf-Sub-Tag)
* template.static
  * style
    * [Use sass file](#template.static | Use Sass)
    * [Prepend section](#template.static | Prepend section)
    * [Final section](#template.static | Final section)
  * script





## Написание адонов

В процесс компиляции можно легко добавить новые структуры.

Основа - Node. Все классы наследованные от класса `rocshelf.template.node.Node` считаются узлами которые могут использоваться при компиляции.

### Регистрация узлов

`rocshelf.template.basic.registration` - функция регистрации нод. После выполнения функции нода становится полноценным учеником компиляции.

### Добавление литерала

### Добавление области видимости

## Использование вне rocshelf

Для использования шаблонизатора rocshelf вне программы нужно учесть следующее:

* Обязательная инициализация логера `mailLogger` модуля rLogging.

Доступные для использования ноды:

* FileNode - Узел компилирующий код из файла указанного при инициализации объекта.
  
  Доступны структуры следующих модулей:

  * template.basic
  * template.operators

* AnalyzeNode - Узел компилирующий код переданный при инициализации объекта.
  
  Доступны структуры следующих модулей:

  * template.basic
  * template.operators

* InputNode - Узел компилирующий код введенный в командную строку после инициализации.
  
  Доступны структуры следующих модулей:

  * template.basic
  * template.operators

## Функциональное описание структур

### template.operators | insert

Вставка. Заменяется на значение в заголовке вызова.

Example:

```html
<!-- vars:
    key = 'value'
    number = 101
    array = [1,2,3]
-->
{i{ key }} = value
{i{ number * 2 }} = 202
{i{ [i * 2 for i in array] }} = [2, 4, 6]
{i{ ', '.join([i * 2 for i in array]) }} = 2, 4, 6
```

### template.operators | insert or default

Вставка со значением по умолчанию. Если при обработки структуры она выдаст исключение, например NameError, TypeError, ConnectionAbortedError,
то вместо завершения компиляции, структура замениться на значение по умолчанию.

Example:

```html
<!-- vars:
    array = [1,2,3]
-->
{i{ 1 + 1 }{ aboba }} = 2
{i{ 1 + 'bruh' }{ aboba }} = aboba
{i{ array[2] } nope } = 3
{i{ array[3] } nope } = nope
```

### template.operators | if

Условие. Если выполняется условие из заголовка вызова, тело будет участвовать в компиляции, иначе тело будет пропущено.

Example:

```html
<!-- template -->
{if{ True }}
    Code if True
{{ }if}

<!-- compiled -->
Code if True
```

### template.operators | else

Не выполненное условие

Example:

```html
<!-- template -->
{if{ False }}
    Code if True
{else{ }}
    Code if False
{{ }if}

equal this:

{if{ False }}
    Code if True
    {else{ }}
        Code if False
    {{ }else}
{{ }if}

<!-- compiled -->
Code if False

equal this:

Code if False
```

### template.operators | elif

При невыполнении первого условия, будет задействовано следующее

Example:

```html
<!-- template -->
{if{ False }}
    Code if True
{else{ True }}
    Code if False and True
{{ }if}

<!-- compiled -->
Code if False and True
```

### template.operators | for

Цикл. По значению из заголовка вызова будет итерирован код в теле структуры.
Внутри тела структуры будет доступна итерируемая переменная и элементы итерации.

Example:

```html
<!-- template -->
{for{ n in [n * 2 for n in range(0,10) if n % 2 == 0 ] }}
    n = {i{ n }}
{{ }for}

<!-- compiled -->
n = 0 n = 4
n = 8 n = 12
n = 16
```

### template.operators | for-else

Структура цикла, с доп условием: Если итерируемая переменная пустая (не итерируется) - выполняется тело из структуры else

Example:

```html
<!-- template -->
{for{ i in [ ] }}
    n = {i{ n }}
{else{ }}
    Array is empty
{{ }for}

<!-- compiled -->
Array is empty
```

### template.shelves | Shelf-Page

Шелф страницы. По переданному имени открывается файл шефа и компилируется на подобии FileNode.
В цикле компиляции rocshelf используется автоматически.

### template.shelves | Shelf-Wrapper

Шелф обертки. Оборачивает шелф, из которого был вызван, собой. Применят и сохраняет секции.

Допустим вызов нескольких оберток. Они будут применяться в порядке указания.

Example:

```html
<!-- shelf-wrapper template -->
<body>
    <main>
        wrapper main code...
        {wp{ }place}
    </main>
    <footer>
        wrapper footer code...
        {wp{ footer }place}
    </footer>
</body>

<!-- caller template -->
{wp{ shelf-wrapper-name  }}

template main code...

{wp{ footer }s}
    template footer code too...
{s{ }wp}

template main code too...

<!-- compiled -->
<body>
    <main>
        wrapper main code...
        template main code...
        template main code too...
    </main>
    <footer>
        wrapper footer code...
        template footer code too...
    </footer>
</body>
```

### template.shelves | Shelf-Block

Шелф блока кода. Структура вызова заменяется на контент из шелф-файла.

Example:

```html
<!-- shelf-block template -->
block code...

<!-- caller template -->
some code...
{bl{ shelf-block-name }}
some code...

<!-- compiled -->
some code...
block code...
some code...
```

### template.shelves | Shelf-Tag

Допустим вызов нескольких тегов. Они будут применяться в порядке указания.

Example:

```html
<!-- shelf-tag template -->
<span class="tag-class" id="tag-id">
    tag code...
    <strong>{t{ }p}</strong>
</span>

<!-- caller template -->
{tag{ shelf-tag-name }}
<strong class="template-class" id="template-id">
    template code...
<strong>

<!-- compiled -->
<strong class="tag-class template-class" id="template-id">
    tag code...
    <strong>
        template code...
    </strong>
</strong>
```

### template.shelves | Shelf-Sub-Tag

```html
<!-- shelf-tag template -->
<span class="tag-class" id="tag-id">
    tag code...

    <strong>{t{ }p}</strong>

    {t{ sub-tag-name }}
    <span class="sub-tag-class" id="sub-tag-id">
        sub tag code...
        {t{ }p}
    </span>
</span>

<!-- caller template -->
{tag{ shelf-tag-name }}
<>
    template code...

    {t{ sub-tag-name }}
    <strong class="template-class" id="template-id">
        template code...
    <strong>
<>

<!-- compiled -->
<span class="tag-class" id="tag-id">
    tag code...

    <strong>
        template code...
    </strong>

    <strong class="sub-tag-class template-class" id="template-id">
        sub tag code...
        template code...
    </strong>
</span>
```

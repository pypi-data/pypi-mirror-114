# xblock-prismjs
XBlock for Syntax Highlighting with Prism.js

# Installation
This XBlock was tested & designed to work with Juniper release.

```
git clone git@github.com:appsembler/xblock-prismjs.git
```

# Features
- 2 themes for Syntax Highlighting via PrismJS: 
  - Light (Default)
  - Dark (Tomorrow Night)
- Supported Languages:
  - Bash
  - C-like, CSS
  - Go
  - Java, Javascript, JSON
  - Lua
  - Markup
  - Python
  - Ruby
  - Shell, SQL
  - YAML

# Usage

### Step 1: From Studio, add "prism" in the "Advanced Module List"

![Screenshot](docs/img/01advancedSettings.png)

### Step 2: Add "Syntax Highlighter" from your unit
Prism XBlock will display as "Syntax Highlighter"
![Gif](docs/img/02prismComponent.gif)

### Step 3: Customize your code block
Edit the code, set a maximum height, select a language, select a theme
![Gif](docs/img/03editComponent.gif)

### Step 4: Publish 
When you're happy with the changes, click the **Publish** button then **View Live Version** to view the changes in LMS
![Screenshot](docs/img/04publish.png)




---
layout: post
title:  "Emacs-esque M-x in Neovim"
<!-- date:   2022-07-29 11:23:25 -0400 -->
<!-- date:  -->
categories: linux emacs neovim vim
---

<li>{{ page.date | date_to_rfc822 }}</li>

I have been using neovim extensively for a year and a half now and it has a wonderful experience. First class support for lua scripting is proving to be [neovim](https://neovim.io/)'s killer feature. The defaults are great and more recently in version 0.8.0 you can easily create and bind lua functions that leverage all of vim, neovim, and linux shell utilities to keybindings. 

This has always been the case with emacs, a functional system from its roots. With the entire editor  being writing in elisp, you can easily bind whatever elisp function to a keybinding.

This snippet of lua code shows how neovim in many ways is emulating emacs by utilizing lua functions;

```lua 
local keymap = vim.keymap.set
keymap("n", "<A-x>", function()
	require("telescope.builtin").keymaps(require("telescope.themes").get_ivy({
		winblend = 5,
		previewer = false,
	}))
end, { desc = "[/keys] execute keymaps or functions]" })
```

This keybinding works in neovim 0.8.0 with [telescope.nvim](https://github.com/nvim-telescope/telescope.nvim) plugin installed.
Here's the breakdown, whenever `<A-x>` i.e. when the key `Alt + x` is pressed in normal mode, neovim detects that the function `require("telescope.builtin").keymaps()` is being asked to be executed. Neovim then executes the function. The rest of the code is just beautifying the output to emulate the emacs package ivy. Telescope's keymap function is essentially a wrapper around the vim command `verbose map`. See `:verbose nmap ` which shows every custom normal mode mapping and where they are defined. The fact that we can bind functions to keys is really cool and a powerful way to use an editor. This is not a new concept but this implementation is very easy for beginners like myself because the code is all lua. For a example I easily create a new keybinding,

```lua 
vim.keymap.set("n", "<A-y>", function()
	vim.cmd("echo expand('%:p')")
	vim.cmd("let @+ = expand('%:p')")
	vim.cmd('echo "Full path of " . expand(\'%:t\') . " was copied to system clipboard"')
end)
```
This is an old vimrc snippet that I converted to lua, It essentially copies the currently edited neovim buffer full path into the system's clipboard and informs the user of the action. 


## Help
`:h map`
`:h telescope`
`:h vim.keymap.set`

<!-- - nano  -- mediocre editor -->
<!-- - vim   -- great extensible editor but there is vimscript which is uncomprehensible in my opinion -->
<!-- - nvim  -- my personal favorite editor, lua allows for easy extensibility -->
<!-- - emacs -- really an operating system, I am starting to use emacs for org mode and reading emails -->
<!---->

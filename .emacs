;;LOAD_PATH
(add-to-list 'load-path' "~/.emacs.d/site-lisp")
(add-to-list 'load-path' "~/.emacs.d/site-lisp/ruby-mode")
(add-to-list 'load-path' "~/.emacs.d/site-lisp/nxhtml")
(add-to-list 'load-path' "~/.emacs.d/site-lisp/yasnippet")

;;设置背景色为 黑色
;;(set-face-background 'default "black")
;;设置前字体色为绿色
;;(set-foreground-color "green")

;; color
;;(require 'color-theme)
;;  (setp color-theme-is-global t)
;;  (color-theme-initialize)
;;(color-theme-euphoria)
;;(color-theme-classic)
;;  (color-theme-charcoal-black)
;;(color-theme-calm-forest)

;;;;显示行号
(global-linum-mode t)

;;全屏
(global-set-key [f11] 'my-fullscreen)

(defun my-fullscreen ()
  (interactive)
  (x-send-client-message
   nil 0 nil "_NET_WM_STATE" 32
   '(2 "_NET_WM_STATE_FULLSCREEN" 0))
)

;;隐藏工作条
(tool-bar-mode nil)

;;隐藏菜单条
(menu-bar-mode nil)
(global-set-key [f7] 'menu-bar-mode)

;; git
;; (require 'vc-git)
;; (when (featurep 'vc-git) (add-to-list 'vc-handled-backends 'git))
;; (require 'git)
;; (autoload 'git-blame-mode "git-blame"
;;   "Minor mode for incremental blame for Git." t)
;; 滚动条
(scroll-bar-mode nil)

;;自定义窗口放大快捷键
(global-set-key [f8] 'enlarge-window)

(global-set-key [(f5)] 'speedbar)

;; template
(require 'template)
(template-initialize)

;; dict
(require 'showtip)
(require 'sdcv)
(setq sdcv-dictionary-simple-list '("朗道英汉字典5.0"))
(global-set-key (kbd "<f6>") 'sdcv-search-pointer+)
(global-set-key (kbd "C-c d") 'sdcv-search-input)

;;tab切换
(require 'tabbar)
(tabbar-mode)
(global-set-key (kbd "<C-left>") 'tabbar-backward-group)
(global-set-key (kbd "<C-right>") 'tabbar-forward-group)
(global-set-key (kbd "<C-up>") 'tabbar-backward)
(global-set-key (kbd "<C-down>") 'tabbar-forward)

;;python-mode 自动缩进及高亮
(setq auto-mode-alist
 (cons '("\\.py$" . python-mode) auto-mode-alist))

(setq interpreter-mode-alist
 (cons '("python" . python-mode)
 interpreter-mode-alist))

(autoload 'python-mode "python-mode" "Python editing mode." t)
;;; add these lines if you like color-based syntax highlighting
(global-font-lock-mode t)
(setq font-lock-maximum-decoration t)

;;自动补全
(require 'pycomplete)
(setq auto-mode-alist (cons '("\\.py$" . python-mode) auto-mode-alist))
(autoload 'python-mode "python-mode" "Python editing mode." t)
(autoload 'pymacs-load "pymacs" nil t)
(autoload 'pymacs-eval "pymacs" nil t)
(autoload 'pymacs-apply "pymacs")
(autoload 'pymacs-call "pymacs")

(setq interpreter-mode-alist(cons '("python" . python-mode)
                             interpreter-mode-alist))

;; (pymacs-load "ropemacs" "rope-")
;; (setq ropemacs-enable-autoimport t)

;;set ipython as the shell
(setq ipython-command "/usr/bin/ipython")
(require 'ipython)

;;插入当前时间

(defun my-insert-date ()
    (interactive)
    (insert "//")
    (insert (user-full-name))
    (insert "@")
    (insert (format-time-string "%Y/%m/%d %H:%M:%S" (current-time))))
(global-set-key (kbd "<f9>") 'my-insert-date)

;; ;;org设置
;; (require 'org-install)
;; (require 'org-publish)
;; (add-to-list 'auto-mode-alist '("\\.org\\'" . org-mode))
;; (add-hook 'org-mode-hook 'turn-on-font-lock)
;; (add-hook 'org-mode-hook
;; (lambda () (setq truncate-lines nil)))

;; (global-set-key "\C-cl" 'org-store-link)
;; (global-set-key "\C-ca" 'org-agenda)
;; (global-set-key "\C-cb" 'org-iswitchb)

;; ;;保存目录及发布目录
;; (setq org-publish-project-alist
;;       '(("note-org"
;;          :base-directory "/home/wyatt/wlife/org"
;;          :publishing-directory "/home/wyatt/public-html"
;;          :base-extension "org"
;;          :recursive t
;;          :publishing-function org-publish-org-to-html
;;          :auto-index t
;;          :index-filename "index.org"
;;          :index-title "index"
;;          :link-home "index.html"
;;          :section-numbers t
;;       :style "<link rel=\"stylesheet\" href=\"../css/emacs.css\" type=\"text/css\"/>"
;;       )

;;         ("note-static"
;;          :base-directory "/home/wyatt/wlife/org"
;;          :publishing-directory "/home/wyatt/public-html"
;;          :recursive t
;;          :base-extension "css\\|js\\|png\\|jpg\\|gif\\|pdf\\|mp3\\|swf\\|zip\\|gz\\|txt\\|el"
;;          :publishing-function org-publish-attachment)
;;         ("note"
;;          :components ("note-org" "note-static")
;;          :author "wwq0327@gmail.com"
;;          )))

;;快捷键

(global-set-key (kbd "<f12> p") 'org-publish)

;; ;;html-helper-mode
;; (autoload 'html-helper-mode "html-helper-mode" "Yay HTML" t)
;; (setq auto-mode-alist (cons '("\\.html$" . html-helper-mode) auto-mode-alist))

;; ;;CSS
;; (autoload 'css-mode "css-mode")
;; (setq auto-mode-alist
;;      (cons '("\\.css\\'" . css-mode) auto-mode-alist))
;; (setq cssm-indent-function #'cssm-c-style-indenter)

;;代码折叠
;; (add-hook 'python-mode-hook 'my-python-hook)

;; (defun py-outline-level ()
;; "This is so that `current-column` DTRT in otherwise-hidden text"
;; ;; from ada-mode.el
;; (let (buffer-invisibility-spec)
;;     (save-excursion
;;       (skip-chars-forward "\t ")
;;       (current-column))))

;; ; this fragment originally came from the web somewhere, but the outline-regexp
;; ; was horribly broken and is broken in all instances of this code floating
;; ; around. Finally fixed by Charl P. Botha <<a href="http://cpbotha.net/">http://cpbotha.net/</a>>
;; (defun my-python-hook ()
;; (setq outline-regexp "[^ \t\n]\\|[ \t]*\\(def[ \t]+\\|class[ \t]+\\)")
;; ; enable our level computation
;; (setq outline-level 'py-outline-level)
;; ; do not use their \C-c@ prefix, too hard to type. Note this overides
;; ;some python mode bindings
;; (setq outline-minor-mode-prefix "\C-c")
;; ; turn on outline mode
;; (outline-minor-mode t)
;; ; initially hide all but the headers
;; (hide-body)
;; (show-paren-mode 1)
;; )
;; (add-to-list 'load-path' "~/.emacs.d/site-lisp/cedet")
;; (require 'cedet)
;; (add-to-list 'load-path' "~/.emacs.d/site-lisp/ecb")
;; (require 'ecb)

;; (add-to-list 'load-path  "~/.emacs.d/site-lisp/cedet/semantic")
;; (setq semantic-load-turn-everything-on t)

;; txt2tags
(setq auto-mode-alist (append (list
        '("\\.t2t$" . t2t-mode)
        )
        (if (boundp 'auto-mode-alist) auto-mode-alist)
))

(autoload  't2t-mode "txt2tags-mode" "Txt2tags Mode" t)

(custom-set-faces
  ;; custom-set-faces was added by Custom.
  ;; If you edit it by hand, you could mess it up, so be careful.
  ;; Your init file should contain only one such instance.
  ;; If there is more than one, they won't work right.
 '(default ((t (:inherit nil :stipple nil :background "black" :foreground "#00ff00" :inverse-video nil :box nil :strike-through nil :overline nil :underline nil :slant normal :weight normal :height 88 :width normal :foundry "apple" :family "Monaco")))))

;; ;;clisp
;; ;;(setq inferior-lisp-program "/usr/bin/clisp")
;; (setq slime-lisp-implementations
;;       '((sbcl ("/usr/bin/sbcl") :coding-system utf-8-unix)    ;(NAME ("/path/to/imp" "--args") :coding-system)
;;         (clisp ("/usr/bin/clisp") :coding-system utf-8-unix)))

;; (require 'slime)
;; (slime-setup '(slime-fancy))

;; (defun lisp-indent-or-complete (&optional arg)
;;   (interactive "p")
;;   (if (or (looking-back "^\\s-*") (bolp))
;;       (call-interactively 'lisp-indent-line)
;;       (call-interactively 'slime-indent-and-complete-symbol)))
;; (eval-after-load "lisp-mode"
;;   '(progn
;;      (define-key lisp-mode-map (kbd "TAB") 'lisp-indent-or-complete)))

;; ;;自动启动slime
;; (add-hook 'slime-mode-hook
;;           (lambda ()
;;             (unless (slime-connected-p)
;;               (save-excursion (slime)))))

;;;; CC-mode配置  http://cc-mode.sourceforge.net/
(require 'cc-mode)
(c-set-offset 'inline-open 0)
(c-set-offset 'friend '-)
(c-set-offset 'substatement-open 0)

;;;;我的C/C++语言编辑策略

;; (defun my-c-mode-common-hook()
;;   (setq tab-width 4 indent-tabs-mode nil)
;;   (setq c-basic-offset 4)
;;   ;;; hungry-delete and auto-newline
;;   ;;(c-toggle-auto-hungry-state 1)
;;   ;;按键定义
;;   (define-key c-mode-base-map [(control \`)] 'hs-toggle-hiding)
;;   (define-key c-mode-base-map [(return)] 'newline-and-indent)
;;   (define-key c-mode-base-map [(f7)] 'compile)
;;   (define-key c-mode-base-map [(meta \`)] 'c-indent-command)
;;   ;;  (define-key c-mode-base-map [(tab)] 'hippie-expand)
;;   (define-key c-mode-base-map [(tab)] 'my-indent-or-complete)
;;   (define-key c-mode-base-map [(meta ?/)] 'semantic-ia-complete-symbol-menu)
;; ;; ;;预处理设置
;; ;; (setq c-macro-shrink-window-flag t)
;; ;; (setq c-macro-preprocessor "cpp")
;; ;; (setq c-macro-cppflags " ")
;; ;; (setq c-macro-prompt-flag t)
;; ;; (setq hs-minor-mode t)
;; ;; (setq abbrev-mode t)
;; )
;; (add-hook 'c-mode-common-hook 'my-c-mode-common-hook)

;; linux-c-mode
(add-hook `c-mode-hook
`(lambda()
(c-set-style "linux")))

;; ruby
(autoload 'ruby-mode "ruby-mode" "Major mode for ruby files" t)
(add-to-list 'auto-mode-alist '("\\.rb$" . ruby-mode))
(add-to-list 'interpreter-mode-alist '("ruby" . ruby-mode))

(require 'ruby-style)
(add-hook 'c-mode-hook 'ruby-style-c-mode)
(add-hook 'c++-mode-hook 'ruby-style-c-mode)

(setq load-path (cons "~/.emacs.d/site-lisp/emacs-rails" load-path))
(require 'rails)

;;; html, css, js dev
;; (load "~/.emacs.d/site-lisp/nxhtml/autostart.el")

(autoload 'django-html-mumamo-mode "~/.emacs.d/site-lisp/nxhtml/autostart.el")
(setq auto-mode-alist
      (append '(("\\.html?$" . django-html-mumamo-mode)) auto-mode-alist))
(setq mumamo-background-colors nil)
(add-to-list 'auto-mode-alist '("\\.html$" . django-html-mumamo-mode))

(require 'yasnippet) ;; not yasnippet-bundle
(yas/global-mode 1)
(yas/load-directory "~/.emacs.d/mysnippets")
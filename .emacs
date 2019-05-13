;(setq-default c-indent-tabs-mode t     ; Pressing TAB should cause indentation
;              c-indent-level 4         ; A TAB is equivilent to four spaces
;              c-argdecl-indent 0       ; Do not indent argument decl's extra
;              c-tab-always-indent t
;              backward-delete-function nil) ; DO NOT expand tabs when deleting
;(c-add-style "my-c-style" '((c-continued-statement-offset 4))) ; If a statement continues on the next line, indent the continuation by 4

;(defun my-c-mode-hook ()
;  (c-set-style "my-c-style")
;  (c-set-offset 'substatement-open '0) ; brackets should be at same indentation level as the statements they open
 ; (c-set-offset 'inline-open '+)
;;  (c-set-offset 'block-open '+)
;  (c-set-offset 'brace-list-open '+)   ; all "opens" should be indented by the c-indent-level
;  (c-set-offset 'case-label '+))       ; indent case labels by c-indent-level, too
;add-hook 'c-mode-hook 'my-c-mode-hook)
;  (add-hook 'c++-mode-hook 'my-c-mode-hook)

;(add-to-list 'auto-mode-alist '("\\.h\\'" . c++-mode))
;(setq-default c-basic-offset 4)
;(setq c-default-style "bsd"
;      c-basic-offset 4
;      indent-tabs-mode nil)

(setq x-select-enable-primary nil)
(setq x-select-enable-clipboard t)

(defun reload-dotemacs ()
(interactive)
(load-file "~/.emacs"))

(global-set-key (kbd "<f12>") 'reload-dotemacs)
(global-set-key (kbd "<mouse-2>") 'x-clipboard-yank)
(global-set-key (kbd "<f2>") 'save-buffer)
(global-set-key (kbd "<f3>") 'next-multiframe-window)
(global-set-key (kbd "<f5>") 'yank)
(global-set-key (kbd "<f7>") 'clipboard-yank)
(global-set-key (kbd "<f8>") 'kill-region)
(global-set-key (kbd "<f9>") 'compile)

(global-set-key (kbd "C-<tab>") 'next-multiframe-window)
(global-set-key (kbd "S-<delete>") 'kill-region)
(global-set-key (kbd "C-S-z") 'redo)

(global-set-key (kbd "<select>") 'move-end-of-line)
(global-set-key (kbd "<backtab>") 'next-buffer)
(global-set-key (kbd "C-Z") 'redo)
(global-set-key "\C-w" 'clipboard-kill-region)
(global-set-key "\C-z" 'undo)
(global-set-key (kbd "S-?") 'kill-region)

; Fix PG up and PG DWN keys:
(global-set-key [next]
    (lambda () (interactive)
        (condition-case nil (scroll-up)
            (end-of-buffer (goto-char (point-max))))))
(global-set-key [prior]
    (lambda () (interactive)
        (condition-case nil (scroll-down)
            (beginning-of-buffer (goto-char (point-min))))))

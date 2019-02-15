;;; find-file-in-project-autoloads.el --- automatically extracted autoloads
;;
;;; Code:
(add-to-list 'load-path (directory-file-name (or (file-name-directory #$) (car load-path))))

;;;### (autoloads nil "find-file-in-project" "find-file-in-project.el"
;;;;;;  (23345 26275 900259 845000))
;;; Generated autoloads from find-file-in-project.el

(autoload 'ffip-git-diff-current-file "find-file-in-project" "\
Run 'git diff version:current-file current-file'.

\(fn)" nil nil)

(autoload 'ffip-copy-without-change "find-file-in-project" "\
Copy P without change.

\(fn P)" nil nil)

(autoload 'ffip-copy-reactjs-import "find-file-in-project" "\
Create ReactJS link from P and copy the result.

\(fn P)" nil nil)

(autoload 'ffip-copy-org-file-link "find-file-in-project" "\
Create org link from P and copy the result.

\(fn P)" nil nil)

(defvar ffip-find-relative-path-callback 'ffip-copy-without-change "\
The callback after calling `find-relative-path'.")

(autoload 'ffip-project-root "find-file-in-project" "\
Return the root of the project.

\(fn)" nil nil)

(autoload 'ffip-save-ivy-last "find-file-in-project" "\
Save `ivy-last' into `ffip-ivy-last-saved'.  Requires ivy.

\(fn)" t nil)

(autoload 'ffip-get-project-root-directory "find-file-in-project" "\
Get the full path of project root directory.

\(fn)" nil nil)

(autoload 'ffip-ivy-resume "find-file-in-project" "\
Wrapper of `ivy-resume'.  Resume the search saved at `ffip-ivy-last-saved'.

\(fn)" t nil)

(autoload 'ffip-filename-identity "find-file-in-project" "\
Return identical KEYWORD.

\(fn KEYWORD)" nil nil)

(autoload 'ffip-filename-camelcase-to-dashes "find-file-in-project" "\
Convert KEYWORD from camel cased to dash seperated.
If CHECK-ONLY is true, only do the check.

\(fn KEYWORD &optional CHECK-ONLY)" nil nil)

(autoload 'ffip-filename-dashes-to-camelcase "find-file-in-project" "\
Convert KEYWORD from dash seperated to camel cased.
If CHECK-ONLY is true, only do the check.

\(fn KEYWORD &optional CHECK-ONLY)" nil nil)

(autoload 'ffip-completing-read "find-file-in-project" "\
Read a string in minibuffer, with completion.

PROMPT is a string with same format parameters in `ido-completing-read'.
COLLECTION is a list of strings.

ACTION is a lambda function to call after selecting a result.

This function returns the selected candidate or nil.

\(fn PROMPT COLLECTION &optional ACTION)" nil nil)

(autoload 'ffip-project-search "find-file-in-project" "\
Return an alist of all filenames in the project and their path.

Files with duplicate filenames are suffixed with the name of the
directory they are found in so that they are unique.

If KEYWORD is string, it's the file name or file path to find file.
If KEYWORD is list, it's the list of file names.
IF IS-FINDING-DIRECTORY is t, we are searching directories, else files.
DIRECTORY-TO-SEARCH specify the root directory to search.

\(fn KEYWORD IS-FINDING-DIRECTORY &optional DIRECTORY-TO-SEARCH)" nil nil)

(autoload 'ffip-find-files "find-file-in-project" "\
Use KEYWORD to find files.
If OPEN-ANOTHER-WINDOW is t, the results are displayed in a new window.
If FIND-DIRECTORY is t, only search directories.  FN is callback.
This function is the API to find files.

\(fn KEYWORD OPEN-ANOTHER-WINDOW &optional FIND-DIRECTORY FN)" nil nil)

(autoload 'ffip-create-project-file "find-file-in-project" "\
Create or Append .dir-locals.el to set up per directory.
You can move .dir-locals.el to root directory.
See (info \"(Emacs) Directory Variables\") for details.

\(fn)" t nil)

(autoload 'ffip-current-full-filename-match-pattern-p "find-file-in-project" "\
Is current full file name (including directory) match the REGEX?

\(fn REGEX)" nil nil)

(autoload 'find-file-in-project "find-file-in-project" "\
More powerful and efficient `find-file-in-project-by-selected' is recommended.

Prompt with a completing list of all files in the project to find one.
If OPEN-ANOTHER-WINDOW is not nil, the file will be opened in new window.
The project's scope is defined as the first directory containing
a `ffip-project-file' whose value is \".git\" by default.
You can override this by setting the variable `ffip-project-root'.

\(fn &optional OPEN-ANOTHER-WINDOW)" t nil)

(autoload 'find-file-in-project-at-point "find-file-in-project" "\
Find file whose name is guessed around point.
If OPEN-ANOTHER-WINDOW is not nil, the file will be opened in new window.

\(fn &optional OPEN-ANOTHER-WINDOW)" t nil)

(autoload 'find-file-in-current-directory "find-file-in-project" "\
Like `find-file-in-project'.  But search only in current directory.
IF OPEN-ANOTHER-WINDOW is t, results are displayed in new window.

\(fn &optional OPEN-ANOTHER-WINDOW)" t nil)

(autoload 'find-file-in-project-by-selected "find-file-in-project" "\
Same as `find-file-in-project' but more poweful and efficient.
It use string from selected region to search files in the project.
If no region is selected, you could provide a keyword.

Keyword could be ANY part of the file's full path and support wildcard.
For example, to find /home/john/proj1/test.js, below keywords are valid:
- test.js
- roj1/tes
- john*test

If keyword contains line number like \"hello.txt:32\" or \"hello.txt:32:\",
we will move to that line in opened file.

If keyword is empty, it behaves same as `find-file-in-project'.

If OPEN-ANOTHER-WINDOW is not nil, the file will be opened in new window.

\(fn &optional OPEN-ANOTHER-WINDOW)" t nil)

(autoload 'find-file-with-similar-name "find-file-in-project" "\
Use base name of current file as keyword which could be further stripped.
by `ffip-strip-file-name-regex'.
If OPEN-ANOTHER-WINDOW is not nil, the file will be opened in new window.

\(fn &optional OPEN-ANOTHER-WINDOW)" t nil)

(autoload 'find-file-in-current-directory-by-selected "find-file-in-project" "\
Like `find-file-in-project-by-selected' but search current directory.
If OPEN-ANOTHER-WINDOW is not nil, the file will be opened in new window.

\(fn &optional OPEN-ANOTHER-WINDOW)" t nil)

(autoload 'find-relative-path "find-file-in-project" "\
Find file/directory and copy its relative path into `kill-ring'.
Optional prefix FIND-DIRECTORY copy the directory path; file path by default.

You can set `ffip-find-relative-path-callback' to format the string before copying,
  (setq ffip-find-relative-path-callback 'ffip-copy-reactjs-import)
  (setq ffip-find-relative-path-callback 'ffip-copy-org-file-link)

\(fn &optional FIND-DIRECTORY)" t nil)

(autoload 'find-directory-in-project-by-selected "find-file-in-project" "\
Similar to `find-file-in-project-by-selected'.
Use string from selected region to find directory in the project.
If no region is selected, you need provide keyword.

Keyword could be directory's base-name only or parent-directoy+base-name
For example, to find /home/john/proj1/test, below keywords are valid:
- test
- roj1/test
- john*test

If OPEN-ANOTHER-WINDOW is not nil, the file will be opened in new window.

\(fn &optional OPEN-ANOTHER-WINDOW)" t nil)

(defalias 'ffip 'find-file-in-project)

(autoload 'ffip-split-window-horizontally "find-file-in-project" "\
Find&Open file in horizontal split window.
New window size is looked up in `ffip-window-ratio-alist' by RATIO.
Keyword to search new file is selected text or user input.

\(fn &optional RATIO)" t nil)

(autoload 'ffip-split-window-vertically "find-file-in-project" "\
Find&Open file in vertical split window.
New window size is looked up in `ffip-window-ratio-alist' by RATIO.
Keyword to search new file is selected text or user input.

\(fn &optional RATIO)" t nil)

(autoload 'ffip-diff-quit "find-file-in-project" "\
Quit.

\(fn)" t nil)

(autoload 'ffip-diff-find-file "find-file-in-project" "\
File file(s) in current hunk.
If OPEN-ANOTHER-WINDOW is not nil, the file will be opened in new window.

\(fn &optional OPEN-ANOTHER-WINDOW)" t nil)

(autoload 'ffip-show-diff-internal "find-file-in-project" "\
Show the diff output by excuting selected `ffip-diff-backends'.
NUM is the index selected backend from `ffip-diff-backends'.
NUM is zero based whose default value is zero.

\(fn &optional NUM)" t nil)

(autoload 'ffip-show-diff-by-description "find-file-in-project" "\
Show the diff output by excuting selected `ffip-diff-backends.
NUM is the backend index of `ffip-diff-backends'.
If NUM is not nil, the corresponding backend is executed directly.

\(fn &optional NUM)" t nil)

(autoload 'ffip-diff-apply-hunk "find-file-in-project" "\
Apply current hunk in `diff-mode'.  Try to locate the file to patch.
Similar to `diff-apply-hunk' but smarter.
Please read documenation of `diff-apply-hunk' to get more details.
If REVERSE is t, applied patch is reverted.

\(fn &optional REVERSE)" t nil)

;;;***

;; Local Variables:
;; version-control: never
;; no-byte-compile: t
;; no-update-autoloads: t
;; End:
;;; find-file-in-project-autoloads.el ends here

# DotfilesSwaper

A simple GUI app to manage your Linux dotfiles and swap them when you want to change things a bit

---

###### **IMPORTANT: THIS SOFTWARE COMES WITH NO WARRANTY!** Make sure to backup all your dotfiles and important system files without using it. Since this software tempers with these files, there is a small chance that it may cause issues by modifying or deleting these files by accident.

---

## How to use:

Clone this repository somewhere in your user files. Launch the app by executing the "interface.pyw" program with Python 3 (use a reasonably recent version, and installed the required libraries).

On the top, you can set your dotfiles directory if the default value isn't correct. You can also open the profiles folder in an external window if you want to manually edit them.

You can create a new profile. You'll be asked a profile name, a description (optional), and an image banner (optional). The software will then copy your current dotfiles into the newly created profile.

You can delete it, but also edit the profile, which allows to change its name, description, banner, and allows you to update the profile files, which will copy your current dotfiles into it.

From the main interface, you can load a profile. Wait until you see a popup window confirming that it has been loaded successfully. It is recommended to close other running apps when loading a profile, as it will delete and replace your currently set dotfiles during the procedure.

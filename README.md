<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<div style="text-align: center;">
  <a href="https://github.com/itskreisler/discord-bot">
    <!--<img src="images/logo.png" alt="Logo" width="80" height="80">-->
    <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-robot" width="100" height="100" viewBox="0 0 24 24" stroke-width="1.5" stroke="#009988" fill="none" stroke-linecap="round" stroke-linejoin="round">
      <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
      <path d="M6 4m0 2a2 2 0 0 1 2 -2h8a2 2 0 0 1 2 2v4a2 2 0 0 1 -2 2h-8a2 2 0 0 1 -2 -2z" />
      <path d="M12 2v2" />
      <path d="M9 12v9" />
      <path d="M15 12v9" />
      <path d="M5 16l4 -2" />
      <path d="M15 14l4 2" />
      <path d="M9 18h6" />
      <path d="M10 8v.01" />
      <path d="M14 8v.01" />
    </svg>
  </a>

<h3 style="text-align: center;">Discord-Bot-Template</h3>

<p style="text-align: center;">
A simple discord bot template to get you started with your own bot!

<!-- <br />

<a href="https://github.com/itskreisler/discord-bot">

<strong>Explore the docs »</strong>
</a>

<br />

<br /> -->
<!-- <a href="https://github.com/itskreisler/discord-bot">View Demo</a>
·
<a href="https://github.com/itskreisler/discord-bot/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
·
<a href="https://github.com/itskreisler/discord-bot/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a> -->
</p>
</div>

## Setup Termux & Terminal

```bash
# update and upgrade
pkg update && pkg upgrade
# install git, binutils and python
pkg install git binutils python
# create venv
python -m venv venv # | Window
virtualenv pyp-env # | Window | Linux | Mac
# activating pyp-env | Window
pyp-env\Scripts\activate
# activating pyp-env | Linux | Mac
source pyp-env/bin/activate
# install requirements
pip install -r requirements.txt
# run the bot
python main.py # | Window
python3 main.py # | Linux
```

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/itskreisler/discord-bot.svg?style=for-the-badge
[contributors-url]: https://github.com/itskreisler/discord-bot/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/itskreisler/discord-bot.svg?style=for-the-badge
[forks-url]: https://github.com/itskreisler/discord-bot/network/members
[stars-shield]: https://img.shields.io/github/stars/itskreisler/discord-bot.svg?style=for-the-badge
[stars-url]: https://github.com/itskreisler/discord-bot/stargazers
[issues-shield]: https://img.shields.io/github/issues/itskreisler/discord-bot.svg?style=for-the-badge
[issues-url]: https://github.com/itskreisler/discord-bot/issues
[license-shield]: https://img.shields.io/github/license/itskreisler/discord-bot.svg?style=for-the-badge
[license-url]: https://github.com/itskreisler/discord-bot/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/kreisler

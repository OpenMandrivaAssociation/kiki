Summary:	The nanobot
Name:		kiki
Version:	1.0.2
Release:	16
License:	Public Domain
Group:		Games/Puzzles
Url:		http://kiki.sourceforge.net/
Source0:	%{name}-%{version}-src.tgz
Source2:	%{name}-story.txt
Source3:	http://kiki.cvs.sourceforge.net/*checkout*/kiki/kiki/sounds/title_song.mp3
Source11:	%{name}-16x16.png
Source12:	%{name}-32x32.png
Source13:	%{name}-48x48.png
Patch0:		kiki-1.0.2-mdkconf.patch
Patch1:		kiki-1.0.2-python-dynling-fix.patch
Patch2:		kiki-1.0.2-gcc4-fix.patch
Patch3:		kiki-1.0.2-python2.5-fix.patch
Patch4:		kiki-1.0.2-define-path.patch
Patch5:		kiki-1.0.2-64-bit-fixes.patch
Patch6:		kiki-1.0.2-gcc432-fix.patch
Patch7:		kiki-1.0.2-initialize-with-glutInit.patch
BuildConflicts:	swig
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(glut)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(SDL_mixer)
BuildRequires:	pkgconfig(SDL_image)

%description
"kiki the nano bot" is a 3-D puzzle game, basically a mixture
of the games Sokoban and Kula-World.

kiki has won the Categories 'Best Graphics', 'Best Originality'
and 'Best Overall Game' in the uDevGame Game Programming Contest 2002.

%prep
%setup -qn %{name}
%apply_patches

cp %{SOURCE2} story.txt
rm -rf `find -type d -name CVS`
for f in `find -type f -name \*.cpp -o -name \*.h -o -name \*.py`; do
	grep -q -Ilsr $'\r$' "$f" && sed -e 's/\r$//' -i "$f"
done

%build
cd kodilib/linux; %make OPTFLAGS="%{optflags}" PYTHONHOME=%{py_platlibdir}; cd -
cd linux; %make OPTFLAGS="%{optflags}" KIKI_HOME="%{_gamesdatadir}/%{name}" PYTHON_VERSION=%{python_version} PYTHONHOME=%{py_platlibdir} GLLIBS="-lglut -lGLU -lGL"; cd -

%install
install -m755 linux/%{name} -D %{buildroot}%{_gamesbindir}/%{name}

install -d %{buildroot}%{_gamesdatadir}/%{name}
cp -r sound py %{buildroot}%{_gamesdatadir}/%{name}
install -m644 %{SOURCE3} -D %{buildroot}%{_gamesdatadir}/%{name}/sound/title_song.mp3

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=%{summary}
Comment=%{summary}
Exec=%{_gamesbindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=Game;LogicGame;X-MandrivaLinux-MoreApplications-Games-Puzzles;
EOF

install -m644 %{SOURCE11} -D %{buildroot}%{_miconsdir}/%{name}.png
install -m644 %{SOURCE12} -D %{buildroot}%{_iconsdir}/%{name}.png
install -m644 %{SOURCE13} -D %{buildroot}%{_liconsdir}/%{name}.png

%files
%doc linux/Readme.txt story.txt Thanks.txt uDevGame\ Readme.txt
%{_gamesbindir}/%{name}*
%{_gamesdatadir}/%{name}
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_datadir}/applications/%{name}.desktop

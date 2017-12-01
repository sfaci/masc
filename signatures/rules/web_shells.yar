rule GIF_exploit
{
meta:
	author = "@patrickrolsen"
	maltype = "GIF Exploits"
	version = "0.1"
	reference = "code.google.com/p/caffsec-malware-analysis"
	date = "2013-12-14"
strings:
	$magic = {47 49 46 38 ?? 61} // GIF8<version>a
	$s1 = "; // md5 Login" nocase
	$s2 = "; // md5 Password" nocase
	$s3 = "shell_exec"
	$s4 = "(base64_decode"
	$s5 = "<?php"
	$s6 = "(str_rot13"
	$s7 = ".exe"
	$s8 = ".dll"
	$s9 = "eval($_"
condition:
	($magic at 0) and any of ($s*)
}

rule html_exploit_GIF
{
meta:
	author = "@patrickrolsen"
	maltype = "Web Shells"
	version = "0.1"
	reference = "code.google.com/p/caffsec-malware-analysis"
	date = "2013-12-14"
strings:
	$magic = {47 49 46 38 ?? 61} // GIF8<version>a
	$s1 = {3c 68 74 6d 6c 3e} // <html>
	$s2 = {3c 48 54 4d 4c 3e} // <HTML>
condition:
	($magic at 0) and (any of ($s*))
}

rule web_shell_crews
{
meta:
	author = "@patrickrolsen"
	maltype = "Web Shell Crews"
	version = "0.6"
	reference = "http://www.exploit-db.com/exploits/24905/"
	date = "08/19/2014"
strings:
	$s1 = "v0pCr3w"
	$s2 = "BENJOLSHELL"
	$s3 = "EgY_SpIdEr"
	$s4 = "<title>HcJ"
	$s5 = "0wn3d"
	$s6 = "OnLy FoR QbH"
	$s7 = "wSiLm"
	$s8 = "b374k r3c0d3d"
	$s9 = "x'1n73ct|d"
	$s10 = "## CREATED BY KATE ##"
	$s11 = "Ikram Ali"
	$s12 = "FeeLCoMz"
	$s13 = "s3n4t00r"
	$s14 = "FaTaLisTiCz_Fx"
	$s15 = "feelscanz.pl"
	$s16 = "##[ KONFIGURASI"
	$s17 = "Created by Kiss_Me"
	$s18 = "Casper_Cell"
	$s19 = "# [ CREWET ] #"
	$s20 = "BY MACKER"
	$s21 = "FraNGky"
	$s22 = "1dt.w0lf"
	$s23 = "Modification By iFX"
	$s24 = "Dumped by C99madShell.SQL"
	$s25 = "Hacked By Alaa"
	$s26 = "XXx_Death_xXX"
	$s27 = "zehir3"
	$s28 = "zehirhacker"
	$s29 = "Shell Tcrew"
	$s30 = "w4ck1ng"
	$s31 = "TriCkz"
	$s32 = "TambukCrew"
	$s33 = "Dumped by c100.SQL"
	$s34 = "Hacker By Task QQ"
	$s35 = "JyHackTeam"
	$s36 = "byMesaj"
	$s37 = "by STHx"
	$s38 = "hacker!@#"
	$s39 = "Fucked by 7sign"
	$s40 = "Hacked By:NsQk"
	$s41 = "Ch1na HLD Secur1ty Team"
	$s42 = "hackxsy.net"
	$s43 = "[Black Tie]"
	$s44 = "[ Black Tie ]"
	$s45 = "X4ck By Death"
	$s46 = "Recoded bY 0x14113"
	$s47 = "0x14113_Server Shell"
	$s48 = "BY 0x14113"
	$s49 = "[ 0x14113 ASP Shell ]"
	$s50 = "ASP Shell"
	$s51 = "Hacked by @iSecGroup"
	$s52 = "@iSecGroup"
	$s53 = "Lulzsecroot"
	$s54 = "KingDefacer"
	$s55 = "Turkish H4CK3RZ"
	$s56 = "by q1w2e3r4"
	$s57 = "By Ironfist"
	$s58 = "AK-74 Security"
	$s59 = "ak74-team.net"
	$s60 = "ANTICHAT.RU" nocase
	$s61 = "ADMINSTRATORS TOOLKIT"
	$s62 = "ASPSpyder"
	$s63 = "Shell v 2.1 Biz"
	$s64 = "Ayyildiz Tim"
	$s65 = "b374k"
	$s66 = "Cool Surfer"
	$s67 = "vINT 21h"
	$s68 = "c0derz shell"
	$s69 = "Emperor Hacking TEAM"
	$s70 = "Comandos Exclusivos"
	$s71 = "Gamma Group"
	$s72 = "GFS Web-Shell"
	$s73 = "Group Freedom Search"
	$s74 = "h4ntu shell"
	$s75 = "powered by tsoi"
	$s76 = "SaNaLTeRoR"
	$s77 = "inDEXER"
	$s78 = "ReaDer"
	$s79 = "JspWebshell"
	$s80 = "zero.cnbct.org"
	$s81 = "Aventis KlasVayv"
	$s82 = "KlasVayv" nocase
	$s82 = "Kodlama by BLaSTER"
	$s83 = "TurkGuvenligi"
	$s84 = "BLaSTER"
	$s85 = "lama's'hell"
	$s86 = "Liz0ziM"
	$s87 = "Loader'z WEB Shell"
	$s88 = "Loader Pro-Hack.ru"
	$s89 = "D3vilc0de"
	$s90 = "lostDC shell"
	$s91 = "MAX666"
	$s92 = "Hacked by Silver"
	$s93 = ".:NCC:."
	$s94 = "National Cracker Crew"
	$s95 = "n-c-c.6x.to"
	$s96 = "Cr4sh_aka_RKL"
	$s97 = "PHANTASMA"
	$s98 = "NeW CmD"
	$s99 = "z0mbie"
	$s100 = "phpRemoteView"
	$s101 = "php.spb.ru"
	$s102 = "Mehdi"
	$s103 = "HolyDemon"
	$s104 = "infilak"
	$s105 = "Rootshell"
	$s106 = "Emperor"
	$s107 = "Iranian Hackers"
	$s108 = "G-Security"
	$s109 = "by DK"
	$s110 = "Simorgh"
	$s111 = "SimShell"
	$s112 = "AventGrup"
	$s113 = "Sincap"
	$s114 = "zyklon"
	$s115 = "lovealihack"
	$s116 = "alihack"
condition:
	not uint16(0) == 0x5A4D and any of ($s*)
}

rule misc_php_exploits
{
meta:
	author = "@patrickrolsen"
	version = "0.5"
	data = "08/19/2014"
	reference = "Virus Total Downloading PHP files and reviewing them..."
strings:
	$php = "<?php" nocase
	$s1 = "eval(gzinflate(str_rot13(base64_decode("
	$s2 = "eval(base64_decode("
	$s3 = "eval(gzinflate(base64_decode("
	$s4 = "cmd.exe /c"
	$s5 = "eva1"
	$s6 = "urldecode(stripslashes("
	$s7 = "preg_replace(\"/.*/e\",\"\\x"
	$s8 = "<?php echo \"<script>"
	$s9 = "'o'.'w'.'s'" // 'Wi'.'nd'.'o'.'w'.'s'
	$s10 = "preg_replace(\"/.*/\".'e',chr"
	$s11 = "exp1ode"
	$s12 = "cmdexec(\"killall ping;"
	$s13 = "ms-mx.ru"
	$s14 = "N3tsh_"
	$s15 = "eval(\"?>\".gzinflate(base64_decode("
	$s16 = "Your MySQL database has been backed up"
	$s17 = "Idea Conceived By"
	$s18 = "ncftpput -u $ftp_user_name -p $ftp_user_pass"
	$s19 = "eval(gzinflate(base64_decode("
	$s20 = "DTool Pro"
condition:
	not uint16(0) == 0x5A4D and $php and any of ($s*)
}

rule zend_framework
{
meta:
	author = "@patrickrolsen"
	maltype = "Zend Framework"
	version = "0.3"
	date = "12/29/2013"
strings:
	$php = "<?php"
	$s = "$zend_framework" nocase
condition:
	not uint16(0) == 0x5A4D and $php and $s
}

rule jpg_web_shell
{
meta:
	author = "@patrickrolsen"
	version = "0.1"
	data = "12/19/2013"
	reference = "http://www.securelist.com/en/blog/208214192/Malware_in_metadata"
strings:
	$magic = { ff d8 ff e? } // e0, e1, e8
	$s1 = "<script src"
	$s2 = "/.*/e"
	$s3 = "base64_decode"
condition:
	($magic at 0) and 1 of ($s*)
}  

rule misc_shells
{
meta:
	author = "@patrickrolsen"
	version = "0.3"
	data = "08/19/2014"
strings:
	$s1 = "second stage dropper"
	$s2 = "SO dumped "
	$s3 = "killall -9 "
	$s4 = "1.sh"
	$s5 = "faim.php"
	$s6 = "file_get_contents("
	$s7 = "$auth_pass ="
	$s8 = "eval($" // Possible FPs
	$s9 = "Find *config*.php"
	$s10 = "Show running services"
	$s11 = "Show computers"
	$s12 = "Show active connections"
	$s13 = "ARP Table"
	$s14 = "Last Directory"
	$s15 = ".htpasswd files"
	$s16 = "suid files"
	$s17 = "writable folders"
	$s18 = "config* files"
	$s19 = "show opened ports"
	$s20 = ".pwd files"
	$s21 = "locate config."
	$s22 = "history files"
	$s23 = "<?php @eval($_POST['cmd']);?>"
	$s24 = "securityprobe.net"
	$s25 = "ccteam.ru"
	$s26 = "c99sh_sources"
	$s27 = "c99mad"
	$s28 = "31373"
	$s29 = "c99_sess_put"
	$s30 = "(\"fs_move_"
	$s31 = "c99sh_bindport_"
	$s32 = "mysql_dump"
	$s33 = "Change this to your password"
	$s34 = "ps -aux"
	$s35 = "p4ssw0rD"
	$s36 = "Ajax Command Shell by"
	$s37 = "greetings to everyone in rootshell"
	$s38 = "We now update $work_dir to avoid things like"
	$s39 = "ls looks much better with"
	$s40 = "I Always Love Sha"
	$s41 = "fileperm=substr(base_convert(fileperms"
	$s42 = "W A R N I N G: Private Server"
	$s43 = "for power security"
	$s44 = "[kalabanga]"
	$s45 = "GO.cgi"
	$s46 = "eval(gzuncompress(base64_decode("
	$s47 = "ls -lah"
	$s48 = "uname -a"
	$s49 = "imageshack.us"
	$s50 = "For Server Hacking"
	$s51 = "Private Exploit"
	$s52 = "chunk_split(base64_encode("
	$s53 = "ending mail to $to......."
	$s54 = "Mysql interface"
	$s55 = "MySQL Database Backup"
	$s56 = "mysql_tool.php?act=logout"
	$s57 = "Directory Lister"
	$s58 = "username and pass here"
	$s59 = "echo base64_decode($"
	$s60 = "get_current_user("
	$s61 = "hey,specify directory!"
	$s62 = "execute command:"
	$s63 = "FILE UPLOADED TO $"
	$s64 = "This server has been infected by"
	$s65 = "Safe_Mode Bypass"
	$s66 = "Safe Mode Shell"
	$s67 = "CMD ExeCute"
	$s68 = "/etc/passwd"
condition:
	not uint16(0) == 0x5A4D and any of ($s*)
}

rule shell_functions
{
meta:
	author = "@patrickrolsen"
	version = "0.1"
	data = "08/19/2014"
	reference = "N/A"
strings:
	$s1 = "function listDatabases()"
	$s2 = "function dropDatabase()"
	$s3 = "mysql_drop_db("
	$s4 = "function listTables()"
	$s5 = "passthru($cmd)"
	$s6 = "function check_file()"
	$s7 = "$id==\"fake-mail\""
	$s8 = "Shell_Exec($cmd)"
	$s9 = "move_uploaded_file("
condition:
	not uint16(0) == 0x5A4D and any of ($s*)
}

rule shell_names
{
meta:
	author = "@patrickrolsen"
	version = "0.3"
	data = "08/19/2014"
	reference = "N/A"
strings:
	$s1 = "faim.php"
	$s2 = "css5.php"
	$s3 = "groanea.php"
	$s4 = "siler.php"
	$s5 = "w.php" fullword
	$s6 = "atom-conf.php"
	$s7 = "405.php"
	$s8 = "pack2.php"
	$s9 = "r57shell.php"
	$s10 = "shell.php" fullword
	$s11 = "dra.php"
	$s12 = "lol.php"
	$s13 = "php-backdoor.php"
	$s14 = "aspxspy.aspx"
	$s15 = "c99.php"
	$s16 = "c99shell.php"
	$s17 = "fx29sh.php"
	$s18 = "azrailphp.php"
	$s19 = "CmdAsp.asp"
	$s20 = "dingen.php"
	$s21 = "entrika.php"
condition:
	not uint16(0) == 0x5A4D and any of ($s*)
}

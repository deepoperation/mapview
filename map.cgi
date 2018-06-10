#!/usr/local/bin/perl

#-------------------------------------------------
#  �ݒ荀��
#-------------------------------------------------

# ���C�u�����捞
require './jcode.pl';
require './cgi-lib.pl';

# �^�C�g����
$title = "���ː�MAP���";

# �^�C�g���̕����F
$t_color = "#804040";

# �^�C�g���̕����T�C�Y
$t_size = '26px';

# �X�N���v�g��URL
$script = './map.cgi';

# �{���̕����t�H���g
$face = '"�l�r �S�V�b�N", "MS UI Gothic", Osaka-mono, Osaka';

# �{���̕����T�C�Y
$b_size = '16px';

# �ǎ����w�肷��ꍇ�ihttp://����w��j
$bg = "";

# �w�i�F���w��
$bc = "#FFFFFF";

# �����F���w��
$tx = "#000000";

$logfile = "log/20110815.log";

# �����N�F���w��
$lk = "#0000FF";	# ���K��
$vl = "#800080";	# �K���
$al = "#FF0000";	# �K�⒆

# �L���� [�^�C�g��] ���̐F
$sub_color = "#880000";

$level0 = 0;
$level1 = 0.2;
$level2 = 0.4;
$level3 = 0.6;
$level4 = 0.8;
$level5 = 1;

#cpm�ƃ�Sv/h�̌������[�g
$exchange_rate = 120;	#�Z�V�E��137�


$logdir = "./log";

#-------------------------------------------------
#  �ݒ芮��
#-------------------------------------------------

# ���C������
&decode;


if ($mode eq "map") {
	&mav_view;
} else {
	&file_list;
}


#-------------------------------------------------
#  �L���\����
#-------------------------------------------------
sub mav_view {
	&header;
	print <<"HTML";
	<div id="map_canvas" style="width:100%; height:100%"></div>
</body>
</html>
HTML
	exit;
}

#-------------------------------------------------
#  �f�R�[�h����
#-------------------------------------------------
sub decode {
	local($key,$val);
	undef(%in);

	&ReadParse;
	while ( ($key,$val) = each(%in) ) {

		next if ($key eq "upfile");

		# �V�t�gJIS�R�[�h�ϊ�
		&jcode'convert(*val, "sjis", "", "z");

		# �^�O����
		$val =~ s/&/&amp;/g;
		$val =~ s/"/&quot;/g;
		$val =~ s/</&lt;/g;
		$val =~ s/>/&gt;/g;

		# ���s����
		$val =~ s/\r\n/<br>/g;
		$val =~ s/\r/<br>/g;
		$val =~ s/\n/<br>/g;

		$in{$key} = $val;
	}
	$mode = $in{'mode'};
	$data = $in{'data'};
	$in{'url'} =~ s/^http\:\/\///;
	if ($in{'sub'} eq "") { $in{'sub'} = "����"; }
}

#-------------------------------------------------
#  BASE64�ϊ�
#-------------------------------------------------
sub base64 {
	local($sub) = @_;
	&jcode'convert(*sub, 'jis', 'sjis');

	$sub =~ s/\x1b\x28\x42/\x1b\x28\x4a/g;
	$sub = "=?iso-2022-jp?B?" . &b64enc($sub) . "?=";
	$sub;
}
sub b64enc {
	local($ch)="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
	local($x, $y, $z, $i);
	$x = unpack("B*", $_[0]);
	for ($i=0; $y=substr($x,$i,6); $i+=6) {
		$z .= substr($ch, ord(pack("B*", "00" . $y)), 1);
		if (length($y) == 2) {
			$z .= "==";
		} elsif (length($y) == 4) {
			$z .= "=";
		}
	}
	$z;
}

#-------------------------------------------------
#  HTML�w�b�_�[
#-------------------------------------------------
sub header {
	$headflag=1;
	open(IN,"./$data") || &error("Open Error: $logfile");
	@input = <IN>;
	$output;
	$i = 0;
	$sievelt;
	
	if($input[0] =~ /exchange_rate/) {
		($dummy,$rate) = split(/:/,$input[0]);
		chomp $rate;
		$exchange_rate = $rate;
		$rate += 0;
		shift(@input);
	}
	
	foreach (@input) {
		($date,$time,$cpm,$lat,$long,$add) = split(/,/);
		# �V�[�x���g���Z
		$sievelt = $cpm / $exchange_rate;
		# �l�̌ܓ�����
		$sievelt *= 100;
		$sievelt += 0.5;
		$sievelt = int $sievelt;
		$sievelt /= 100;
		if($sievelt > $level5) {
			$markerImg = "markerLV6";
		} elsif($sievelt > $level4) {
			$markerImg = "markerLV5";
		} elsif($sievelt > $level3) {
			$markerImg = "markerLV4";
		} elsif($sievelt > $level2) {
			$markerImg = "markerLV3";
		} elsif($sievelt > $level1) {
			$markerImg = "markerLV2";
		} else {
			$markerImg = "markerLV1";
		}
		
#		$print1 = 'var marker' . $i . ' = new google.maps.Marker({position: new google.maps.LatLng(' . $lat . ',' . $long . '), map: map, title:"' . $date . $time . ": " . $sievelt . "��Sv/h" . '"' . ', clickable: true' . ', draggable: true' . '});' . "\n";
		$print1 = 'var marker' . $i . ' = new google.maps.Marker({position: new google.maps.LatLng(' . $lat . ',' . $long . '), map: map, title:"' . $date . "," . $time . ": " . $sievelt . "��Sv/h" . '"' . ', clickable: true' . ', draggable: true' . ", icon: $markerImg" . '});' . "\n";
		$print2 = "var infowindow$i = new google.maps.InfoWindow({ content: '" . $date . " " . $time . "<BR>". $sievelt . "��Sv/h" . ", CPM=" . $cpm . "'});" . "\n";
		$print3 = "google.maps.event.addListener(marker$i, 'click', function() {infowindow$i.open(map,marker$i);});\n";
#		$print4 = "google.maps.event.trigger(marker$i, 'click');\n";
		$i++;
		$output = $output . $print1 . $print2 . $print3 . $print4;
	}
	close(IN);
	print "Content-type: text/html\n\n";
	print <<"EOM";
<html>
<head>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
	<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
	<script type="text/javascript">
		google.maps.event.addDomListener(window, 'load', function() {
			var mapdiv = document.getElementById("map_canvas");
			var myOptions = {
				zoom: 12,
				center: new google.maps.LatLng($lat,$long),
				mapTypeId: google.maps.MapTypeId.ROADMAP,
				scaleControl: true,
			};
			var map = new google.maps.Map(mapdiv, myOptions);
			// �}�[�J�[�摜���쐬 
			var markerLV1 = new google.maps.MarkerImage( 
				"green-dot.png", 
				new google.maps.Size(32, 32), 
				new google.maps.Point(0, 0)
			); 
			var markerLV2 = new google.maps.MarkerImage( 
				"ltblue-dot.png", 
				new google.maps.Size(32, 32), 
				new google.maps.Point(0, 0)
			); 
			var markerLV3 = new google.maps.MarkerImage( 
				"blue-dot.png", 
				new google.maps.Size(32, 32), 
				new google.maps.Point(0, 0)
			); 
			var markerLV4 = new google.maps.MarkerImage( 
				"yellow-dot.png", 
				new google.maps.Size(32, 32), 
				new google.maps.Point(0, 0)
			); 
			var markerLV5 = new google.maps.MarkerImage( 
				"orange-dot.png", 
				new google.maps.Size(32, 32), 
				new google.maps.Point(0, 0)
			); 
			var markerLV6 = new google.maps.MarkerImage( 
				"red-dot.png", 
				new google.maps.Size(32, 32), 
				new google.maps.Point(0, 0)
			);
$output
		});
	</script>
<meta name="robots" content="noarchive">
<STYLE type="text/css">
<!--
body,td,th { font-size:$b_size; font-family:$face }
a:hover { color: $al }
-->
</STYLE>
<title>$title</title></head>
EOM

	if ($bg) {
		print "<body background=\"$bg\" bgcolor=\"$bc\" text=\"$tx\" link=\"$lk\" vlink=\"$vl\" alink=\"$al\">\n";
	} else {
		print "<body bgcolor=\"$bc\" text=\"$tx\" link=\"$lk\" vlink=\"$vl\" alink=\"$al\">\n";
	}
}

#-------------------------------------------------
#  URL�G���R�[�h
#-------------------------------------------------
sub url_enc {
	local($_) = @_;

	s/(\W)/'%' . unpack('H2', $1)/eg;
	s/\s/+/g;
	$_;
}

#-------------------------------------------------
#  �t�@�C�����X�g�\��
#-------------------------------------------------
sub file_list {
	@filelist = `ls $logdir`;
	
	&header;
	print "<ul>";
	
	foreach $dlfile (@filelist){
		$dlfile =~ s/[\r\n]*$//;  # instead of a chop
		$display_file = "$logdir/$dlfile";
		
		($d_dev,$d_ino,$d_mode,$d_nlink,$d_uid,$d_gid,$d_rdev,$d_size,$d_atime,$d_mtime,$d_ctime,$d_blksize,$d_blocks)=stat("$display_file");
		($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst)=localtime($d_mtime);
		$update = sprintf("%s�N%s��%s��%02s��%02s��",$year+1900,$mon+1,$mday,$hour,$min);
		
		if ($d_size > 1048576){
			$size = sprintf("%.1fMB",$d_size/1048576);
		} elsif ($d_size > 1024){
			$size = sprintf("%.1fkB",$d_size/1024);
		} else {
			$size = sprintf("%dB",$d_size);
		}
		print "<li>";
		print "<a href=\"./$script?mode=map&data=$display_file\">$dlfile</a> ($size)";
		print " <font color=\"gray\">.......... $update</font>";
		print "</li>\n";
	}
	print "</ul>\n";
	print "<ul>\n";
	print "�}�[�J�[�̐F�̈Ӗ�<BR>";
	print "$level0��<img src=\"green-dot.png\" alt=\"��\">����$level1��<img src=\"ltblue-dot.png\" alt=\"���F\">����$level2��<img src=\"blue-dot.png\" alt=\"��\">����$level3��<img src=\"yellow-dot.png\" alt=\"��\">����$level4��<img src=\"orange-dot.png\" alt=\"�I�����W\">����$level5��<img src=\"red-dot.png\" alt=\"��\">\n";
	print "</ul>\n";
}


__END__


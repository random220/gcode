$n = 0;
while ($l = <DATA>) {
    chomp $l;
    #$l =~ m{^(.+?)[\s\-]+(\d+)\:(\d+)$};
    ($h, $m, $s, $title) = $l =~ m{^(\d+)\:(\d+)\:(\d+)\s+(.+)$};
    $x = $h * 60 * 60 + 60 * $m + $s;
    $x = $x.'.00000';
    $n++;
    print "$x\t$x\t$n - $title\n";
}
__DATA__
00:00:06 O Mere Dil Ke Chain - Kishore Kumar - R.D. Burman - Majrooh Sultanpuri
00:04:42 Lag Ja Gale Se Phir - Lata Mangeshkar - Madan Mohan - Raja Mehdi Ali Khan
00:09:00 Tere Bina Zindagi Se - Lata Mangeshkar, Kishore Kumar - R.D. Burman - Gulzar
00:14:54 Chura Liya Hai Tumne Jo Dil Ko - Asha Bhosle, Mohammed Rafi - R.D. Burman - Majrooh Sultanpuri
00:19:42 Bheegi Bheegi Raaton Mein - Lata Mangeshkar, Kishore Kumar - R.D. Burman - Anand Bakshi
00:23:31 Ek Ajnabee Haseena Se - Kishore Kumar - R.D. Burman - Anand Bakshi
00:27:57 Tum Aa Gaye Ho Noor Aa Gaya - Lata Mangeshkar, Kishore Kumar - R.D. Burman - Gulzar
00:32:09 Kora Kagaz Tha Yeh Man Mera - Lata Mangeshkar, Kishore Kumar - S.D. Burman - Anand Bakshi
00:37:48 Likhe Jo Khat Tujhe - Mohammed Rafi - Shankar_Jaikishan - Neeraj
00:42:21 Kya Hua Tera Vada - Mohammed Rafi, Sushma Shrestha - R.D. Burman - Majrooh Sultanpuri
00:46:39 Aap Ki Ankhon Mein Kuch - Kishore Kumar, Lata Mangeshkar - R.D. Burman - Gulzar
00:50:48 Yeh Sham Mastani - Kishore Kumar - R.D. Burman - Anand Bakshi
00:55:25 Ajib Dastan Hai Yeh - Lata Mangeshkar - Shankar_Jaikishan - Shailendra
01:00:41 Mere Sapnon Ki Rani - Kishore Kumar - S.D. Burman - Anand Bakshi
01:05:41 Abhi Na Jao Chhod Kar - Asha Bhosle, Mohammed Rafi - Jaidev - Sahir Ludhianvi
01:09:56 Bahon Mein Chale Aao - Lata Mangeshkar - R.D. Burman - Majrooh Sultanpuri
01:13:58 Hamen Tumse Pyar Kitna - Kishore Kumar - R.D. Burman - Majrooh Sultanpuri
01:17:59 Bade Achhe Lagte Hain - Amit Kumar - R.D. Burman - Anand Bakshi
01:23:11 Mere Mehboob Qayamat Hogi - Kishore Kumar - Laxmikant_Pyarelal - Anand Bakshi
01:27:00 Roop Tera Mastana - Kishore Kumar - S.D. Burman - Anand Bakshi
01:30:45 Goom Hai Kisi Ke Pyar Mein - Kishore Kumar, Lata Mangeshkar - R.D. Burman - Majrooh Sultanpuri
01:35:00 Aanewala Pal Janewala Hai - Kishore Kumar - R.D. Burman - Gulzar
01:39:39 Gaata Rahe Mera Dil - Lata Mangeshkar, Kishore Kumar - S.D. Burman - Shailendra
01:44:32 Kisi Ki Muskurahaton Pe - Mukesh - Shankar_Jaikishan - Shailendra
01:49:02 Pyar Hua Iqrar Hua

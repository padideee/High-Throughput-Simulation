#!/usr/bin/perl


$ZINC_smi_in = "ligs.txt";
$FlexAID_LIG_LIST_FILE = "lig_list_new.txt";

while(@ARGV){
  $arg = shift @ARGV;
  if($arg eq "-b"){$batch_stamp   = shift @ARGV;}
  if($arg eq "-s"){$batch_size  = shift @ARGV;}
}


open(IN,$ZINC_smi_in) || die "cannot open $ZINC_smi_in ZINC smile file for read\n";

while($line = <IN>){
  @tmp=split(/\t/,$line);
  push(@ids,$tmp[0]);
  push(@smi,$tmp[1]);
}
close(IN);

$FlexAID_list = "";
print "Number of smile strings(",$#smi,") and IDs (",$#ids,")\n";
if($#smi != $#ids){print "Error: numbers of smile strings and IDs don't match\n"};


$next_batch_stamp = $batch_stamp + $batch_size;
if($#ids <= $next_batch_stamp){$next_batch_stamp = $#ids};
$i=$batch_stamp;

while( $i <=$next_batch_stamp){
  $file=$ids[$i].".smi";
  print($file);

  print $i," ",$ids[$i]," ",@smi[$i]," ",$file;
  open(OUT,">$file");
  print OUT @smi[$i];
  close(OUT);
  if(-e "oblog"){unlink("oblog") or die "cannot delete oblog\n";}

  eval {
    local $SIG{'ALRM'} = sub {die "alarm\n"};
    alarm(30);

    ###################### provide the path to Process_Ligand
    system("/home/padideh/projects/rrg-najmanov/padideh/Process_Ligand -f " . $file . " --gen3D --atom_index9000 > oblog");

    alarm(0);
  };

  open(IN,"oblog");
  $success[$i]=0;
  while($line = <IN>){if($line =~ /Done/){$success[$i]=1;}}
  close(IN);
  if($success[$i] == 0){
    print " ERROR\n";
  }else{
    $file=$ids[$i].".inp";
    $FlexAID_list .= $ids[$i]."\t".@smi[$i];
    $file=$ids[$i].".mol2.tmp";
    unlink($file);
  }
  $i++;
}
open(OUT,">$FlexAID_LIG_LIST_FILE") || die "cannot open $FlexAID_LIG_LIST_FILE FlexAID LIG LIST FILE for write\n";
print OUT $FlexAID_list;
close(OUT);

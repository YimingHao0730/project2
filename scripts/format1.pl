#!/usr/bin/perl -w
use strict;
use Getopt::Long;

my $in_path;
GetOptions('input=s' => \$in_path);
die "Usage: $0 --input <path/to/filename>\n" unless defined $in_path;

my %h;
my $name;
open my $I, "<", $in_path or die "Cannot open $in_path: $!";
while (my $a = <$I>) {
    chomp $a;
    if ($a =~ /^>/) {
        $a =~ s/\s/_/g;
        $name = $a;
    } else {
        $a =~ s/\s//g;
        $h{$a} = $name . "\n" . $a unless exists $h{$a}; # Store only first occurrence to remove redundant sORFs
    }
}
close $I;

# Write the changes back to the file
open my $O, ">", $in_path or die "Cannot open $in_path: $!";
foreach my $seq (keys %h) {
    print $O "$h{$seq}\n"; # Write non-redundant sequences back to file
}
close $O;



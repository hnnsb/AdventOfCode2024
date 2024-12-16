$scriptname = $args[0]

if ($args.Count -gt 1) {
    $scriptparam = $args[1]
    (Measure-Command { python $scriptname $scriptparam | Out-Default }).ToString()
} else {
    (Measure-Command { python $scriptname | Out-Default }).ToString()
}

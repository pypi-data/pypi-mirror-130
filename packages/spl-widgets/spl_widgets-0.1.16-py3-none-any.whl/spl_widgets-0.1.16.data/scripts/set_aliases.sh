#!/bin/zsh
modules_to_alias="update_widgets widgets_help gorilla_clean stk_swx tuner"
for MODULE in $modules_to_alias; do
    alias ${MODULE}="python3 -m spl_widgets ${MODULE}"
done
echo "Done!"
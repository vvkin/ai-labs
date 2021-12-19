(import os
        [numpy :as np]
        [pandas :as pd]
        [lisp.utils [get_script_path]]
)

(setv path (os.path.join (get_script_path) "../../logs/stats.csv"))
(setv df (pd.read_csv path))

(setv score (get df "score"))
(print "Score variance (dispersion):" (.var score))

(setv elapsed (get df "elapsed"))
(print "Elapsed mean:" (.mean elapsed))

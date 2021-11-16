(import os
        [lisp.types [Point]]
)


(defn get_script_path []
  (os.path.dirname(os.path.realpath(get sys.argv 0)))
)

(defn get_layout_path [^str name]
  (setv script_path (get_script_path))
  (setv relative_path (os.path.join script_path "../assets/layouts"))
  (os.path.join relative_path name)
)

(defn add_points [^Point a ^Point b]
  (, (+ (get a 0) (get b 0)) (+ (get a 1) (get b 1)))
)

(defn manhattan [^Point a ^Point b]
  (+ (abs (- (get a 0) (get b 0))) (abs (- (get a 1) (get b 1))))
)

(import os
        [numpy :as np]
        [dataclasses [dataclass]]
)

; define types
(setv Point (of (, int int)))
(setv Maze np.ndarray)
(setv Cost float)
(setv Agent int)

(defclass Move [] 
  (setv DOWN (, 0 1))
  (setv LEFT (, -1 0))
  (setv UP (, 0 -1))
  (setv RIGHT (, 1 0))

  (with-decorator staticmethod 
    (defn as_list []
      [Move.DOWN Move.LEFT Move.UP Move.RIGHT]
    )
  )
)

(defclass Parser [] 
    (with-decorator staticmethod 
      (defn read_layout [^str path] 
        (with [file (open path)] 
          (setv layout (lfor line file (list (line.strip))))
        )
        (np.array layout)
      )
    )

    (with-decorator staticmethod 
      (defn parse_layout [^str path] 
        (setv np_layout (Parser.read_layout path)) 
        (setv maze (= layout "%")) 
        (setv pacman (Parser.get_position layout "P"))
        (setv ghost (Parser.get_position layout "G"))
      )
    )
)

(defclass Layout [] 
  (with-decorator staticmethod 
    (defn read_layout [^str path] 
      (with [file (open path)] 
        (setv layout (lfor line file (list (line.strip))))
      )
      (np.array layout)
    )
  )

  (with-decorator staticmethod 
    (defn load_layout[^str path] 
      (setv layout (Layout.read_layout path))
      (setv maze (= layout "%"))
      (setv pacman (get (np.argwhere (= layout "P")) 0))
      (setv ghost (get (np.argwhere (= layout "G")) 0))
      (, maze [pacman ghost])
    )
  )
)

(defn get_layout_path [^str name]
  (setv script_path (os.path.dirname(os.path.realpath(get sys.argv 0))))
  (setv relative_path (os.path.join script_path "../assets/layouts"))
  (os.path.join relative_path name)
)

(setv layout_path (get_layout_path "minimaxSmall.lay"))
(print layout_path)
(setv layout (Layout.load_layout layout_path))
(print layout)

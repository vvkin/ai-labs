(import [numpy :as np]
        [dataclasses [dataclass]]
        [typing [Any]]
        [lisp.types [Point Maze Cost Agent]]
        [lisp.utils [get_layout_path add_points manhattan]]
)


(defclass Direction [] 
  (setv UP (, 1 0))
  (setv DOWN (, -1 0))
  (setv RIGHT (, 0 1))
  (setv LEFT (, 0 -1))
  (setv STOP (, 0 0))

  (with-decorator staticmethod 
    (defn as_list []
      [Direction.DOWN Direction.LEFT Direction.UP Direction.STOP Direction.RIGHT]
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
      (setv pacman (list (get (np.argwhere (= layout "P")) 0)))
      (setv ghost (list (get (np.argwhere (= layout "G")) 0)))
      (, maze [pacman ghost])
    )
  )
)

(with-decorator (dataclass :eq False)
  (defclass State[] 
    (^Maze maze)
    (^Any agents)
    (setv ^Any last_move None)

    (with-decorator property 
      (defn pacman [self]
        (get self.agents 0)
      )
    )

    (with-decorator property 
      (defn ghost [self]
        (get self.agents 1)
      )
    )

    (with-decorator property 
      (defn is_game_over [self]
        (= self.pacman self.ghost)
      )
    )

    (defn get_moves [self ^Agent agent] 
      (setv position (get self.agents agent))
      (setv moves [])
      (for [move (Direction.as_list)]
        (setv (, x y) (add_points position move))
        (if (not (get (get self.maze y) x))
          (moves.append move)
        )
      )
      moves
    )

    (defn generate_next [self ^Agent agent ^Point move] 
      (setv new_agents (lfor agent self.agents agent))
      (setv new_maze (self.maze.copy))
      (setv position (get self.agents agent))
      (setv (get new_agents agent) (add_points position move))
      (setv last_move (, agent move))
      (State new_maze new_agents last_move)
    )
  )
)

(with-decorator (dataclass :eq False)
  (defclass MinimaxState [] 
    (^State game) 
    (setv ^Agent agent 0)
    (setv ^int depth 0)

    (with-decorator property 
      (defn move [self] 
        (get (. self.game last_move) 1)
      )
    )
  )
)

(with-decorator (dataclass :eq False)
  (defclass MinimaxValue []
    (^int cost)
    (setv ^Point move Direction.STOP)
  )
)

(with-decorator (dataclass :eq False)
  (defclass Minimax [] 
    (setv ^int max_depth 2)

    (defn get_neighbors [self ^MinimaxState state]
      (setv depth (if (= state.agent 0) state.depth (+ state.depth 1)))
      (setv agent (% (+ state.agent 1) 2))

      (setv game state.game)
      (gfor move (game.get_moves state.agent)
        :do (setv next_game (game.generate_next state.agent move))
        (MinimaxState next_game agent depth)
      )
    )

    (defn utility [self ^MinimaxState state]
      (if (. state.game is_game_over) 
        (return (float "inf"))
      )
      (setv pacman (. state.game pacman))
      (setv ghost (. state.game ghost))
      (manhattan pacman ghost)
    )

    (defn is_terminal [self ^MinimaxState state]
      (or (. state.game is_game_over) (= state.depth self.max_depth))
    )

    (defn minimax [self ^MinimaxState state]
      (cond 
        [(self.is_terminal state)
          (MinimaxValue (self.utility state))]
        [(= state.agent 0)
          (self.max_value state)]
        [(= state.agent 1)
          (self.min_value state)]
      )
    )

    (defn min_value [self ^MinimaxState state]
      (setv values 
        (lfor neighbor (self.get_neighbors state) 
          (MinimaxValue (. (self.minimax neighbor) cost) neighbor.move)
        )
      )
      (min values :key (fn [neighbor] neighbor.cost))
    )

    (defn max_value [self ^MinimaxState state]
      (setv values 
        (lfor neighbor (self.get_neighbors state) 
          (MinimaxValue (. (self.minimax neighbor) cost) neighbor.move)
        )
      )
      (max values :key (fn [neighbor] neighbor.cost))
    )

    (defn __call__ [self ^State state]
      (. (self.minimax (MinimaxState state)) move)
    )
  )
)

;; main
(setv layout_path (get_layout_path "minimaxSmall.lay"))
(setv (, maze agents) (Layout.load_layout layout_path))

(print "Maze\n" maze)
(print "Pacman <-> Ghost:" agents)

(setv state (State maze agents))
(setv minimax (Minimax 2))
(setv best_move (minimax state))
(print "Best move:" best_move)

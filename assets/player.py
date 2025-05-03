import pygame
from assets.entity import Entity 
from assets.settings import *
from assets.resources import importFolder
from math import floor, sin, cos, pi
from skill import Skill
from random import randint, choices

from assets.superposedPlayer import SuperposedPlayer

class Player(Entity):
    # Static Variables
    animations = {} 
    frame_index = 0
    animationSpeed = 0.09
    status = "down_idle"
    enabled_movement = True
    speed = 1
    direction = pygame.math.Vector2()
    lives = 3

    def __init__(self, start_pos, groups, obstacleSprites, game):
        super().__init__(groups)
        # Game State
        self.game = game
        self.superposition = False
        self.entangled = False
        self.spriteType = 'player'
        # self.ignoreCollisions = True

        # Graphics Variables
        self.import_player_assets(TEAM[0])
        self.spriteGroups = groups
        self.image = Player.animations[Player.status][int(Player.frame_index)]
        self.rect = self.image.get_rect(topleft = start_pos)
        self.superpositionSprites = [] # Holds superposition sprites

        # Movement and Collision Variables
        self.hitbox = self.rect
        self.hitbox.height -= 5  # Reduce height by 5 pixels
        self.obstacleSprites = obstacleSprites

        # Quantum Spells
        self.currentQuantumSpell = 0
        self.quantumSpellBook = {'X': 0, 'H': 0}

        # ---------------------- Team Attributes ---------------------- #

        self.currentCharacter = 'Q' # self.team[self.character_index]

        # ---------------------- Team Attributes ---------------------- #

        # Attack Variables
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = 0
        self.weapon_index = 0  # weapon type

        self.immune = False
        self.damage_time = 0
        self.i_frames = 500

        # Skill Variables
        if not isinstance(self, SuperposedPlayer):
            self.skill = Skill(self, [groups[0], obstacleSprites])
        self.skill_time = 0
        self.observeTime = 0
        self.can_skill = True
        self.canObserve = True


    def import_player_assets(self, selected_char: str):
        # Adds the selected character's movement animations to self.animations
        character_path = f'assets/player/{selected_char}/'
        Player.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                        'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': []}
                        #    'up_attack': [], 'down_attack': [], 'left_attack': [], 'right_attack': [], }

        for animation in Player.animations.keys():
            complete_path = character_path + animation
            Player.animations[animation] = importFolder(complete_path)

    def user_input(self, actions):
        if not self.attacking or self.enabled_movement:
            # print(Player.direction,self.direction )
            keys = pygame.key.get_pressed()
            left, middle, right = pygame.mouse.get_pressed()
            # ---------- ====== MOVEMENT ====== ---------- #
            self.direction.x = actions["right"] - actions["left"]
            self.direction.y = actions["down"] - actions["up"]
            if actions["up"]:
                Player.status = 'up'
                # self.direction.y = -1
            elif actions["down"]:
                Player.status = 'down'
                # self.direction.y = 1
            if actions["right"]:
                Player.status = 'right'
                # self.direction.x = 1
            elif actions["left"]:
                Player.status = 'left'
                # self.direction.x = -1
            # ---------- ====== MOVEMENT ====== ---------- #

            # ---------- ======= ACTIONS ====== ---------- #
            # ------- Normal Attack ----- #
            # if left:
            #     self.attacking = True
            #     self.attack_time = pygame.time.get_ticks()
            #     self.create_attack()
            # ---------- Skill ---------- #
            if actions["action_e"] and self.can_skill and not self.superposition:
                self.can_skill = False
                self.skill_time = pygame.time.get_ticks()
                self.skill.castCircuit()
            elif actions["action_r"] and self.canObserve:
                self.canObserve = False
                self.observeTime = pygame.time.get_ticks()
                self.skill.observe()
            # ---------- Burst ---------- #
            # if keys[pygame.K_q] and self.can_burst:
            #     self.can_burst = False
            #     self.attack_time = pygame.time.get_ticks()
            #     self.create_burst()
            # ---------- ======= ACTIONS ====== ---------- #

            # ---------- ====== SWAP CHAR ===== ---------- #
            # if not self.character_swapping:
            #     if keys[pygame.K_1]:
            #         self.character_index_new = 0
            #     if keys[pygame.K_2]:
            #         self.character_index_new = 1
            #     if keys[pygame.K_3]:
            #         self.character_index_new = 2
            #     if keys[pygame.K_4]:
            #         self.character_index_new = 3
            #     if keys[pygame.K_1] or keys[pygame.K_2] or keys[pygame.K_3] or keys[pygame.K_4]:
            #         self.character_swapping = True
            #         self.character_swap_time = pygame.time.get_ticks()
            #         self.character_swap()
            # ---------- ====== SWAP CHAR ===== ---------- #

    def get_status(self):
        # Idle Status
        # print(Player.status)
        if self.direction.x == 0 and self.direction.y == 0:
            if 'idle' not in Player.status and 'attack' not in Player.status:
                Player.status = Player.status + '_idle'

        # Attack Status
        # if self.attacking:
        #     self.direction.x = 0
        #     self.direction.y = 0
        #     if 'attack' not in self.status:
        #         if 'idle' in self.status:
        #             self.status = self.status.replace('_idle', '_attack')
        #         else:
        #             self.status = self.status + '_attack'
        # else:
        #     self.status = self.status.removesuffix('_attack')

    def character_cooldowns(self):  # attack cooldown
        start_time = pygame.time.get_ticks()

    #     # Character Cooldown
    #     if self.character_swapping:
    #         if start_time - self.character_swap_time >= 400:  # 400 ticks cooldown
    #             self.character_swapping = False
    #     # Attack Cooldown
    #     if self.attacking:
    #         if start_time - self.attack_time >= WEAPON_DATA[self.current_char.weapon_type]['cooldown']:  # 400 ticks
    #             # cooldown
    #             self.attacking = False
    #             self.destroy_attack()
    #     # Skill Cooldown
        if not self.can_skill:
            self.can_skill = start_time - self.skill_time >= 1000
        if not self.canObserve:
            self.canObserve = start_time - self.observeTime >= 800

    def character_animation(self):
        animation = Player.animations[Player.status]

        # Iterate through the animation list each method call
        Player.frame_index += Player.animationSpeed
        if Player.frame_index >= len(animation):
            Player.frame_index = 0

        self.image = animation[int(Player.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        # Handle Alpha Value
        if self.superposition:
            self.image.set_alpha(0)
        elif self.immune:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def enterSuperposition(self):
        self.superposition = True
        self.ignoreCollisions = True
        distance = 65
        possibilities = 2**self.game.stateStack[-1].qubitNo
        for i in range(possibilities):
            start_pos = pygame.math.Vector2(self.rect.x, self.rect.y)
            offset = pygame.math.Vector2(distance*sin(i * (2*pi) / possibilities), -distance*cos(i * (2*pi) / possibilities))
            start_pos += offset
            istate = SuperposedPlayer(self.spriteGroups, self.obstacleSprites, self, offset, i) 
            self.superpositionSprites.append(istate)

    def collapseSuperposition(self):
        self.superposition = False
        self.ignoreCollisions = False
        distance = 65
        collapsedState = self.nonCollidedPossibleState()
        oldPos = self.hitbox.center
        if collapsedState != -1:
            self.hitbox.x += distance * (collapsedState%2 * (2-collapsedState))
            self.hitbox.y += distance * (-1 * ((collapsedState+1)%2) * (1-collapsedState))
            self.rect.center = self.hitbox.center
        else: self.rect.center = oldPos

        if self.collided: self.rect.center = oldPos
        for sprite in self.superpositionSprites:
            sprite.kill()
        self.superpositionSprites = []

    def update(self):
        # self.update_character_stats()
        # if not isinstance(self, SuperposedPlayer):
        self.user_input(self.game.actions)
        self.character_cooldowns()
        self.get_status()
        # print(self.collided)
        
        if self.enabled_movement: 
            self.move(Player.speed)
            self.character_animation()


        # elif isinstance(self, SuperposedPlayer):
            # self.superimposed_animation(255)

    def nonCollidedPossibleState(self):
        probabilities = self.game.stateStack[-1].quantumComputer.probabilities
        nonCollidedPossibleStates = []
        for i in range(len(probabilities)):
            # print(f"prob[{i}]: {probabilities[i]}")
            if probabilities[i] > 0 and i < len(self.superpositionSprites):
                # print(f"{i}: {self.superpositionSprites[i].collided}, amp: {self.superpositionSprites[i].amplitude}")
                if self.superpositionSprites[i].collided != False and self.superpositionSprites[i].amplitude:
                    nonCollidedPossibleStates.append(i)
        # print(f"Non Collided Possible States: {nonCollidedPossibleStates}")
        if len(nonCollidedPossibleStates) <= 0: return -1

        # Filter probabilities and normalize
        filtered_probs = [probabilities[i] for i in nonCollidedPossibleStates]
        total = sum(filtered_probs)
        normalized_probs = [p / total for p in filtered_probs]

        selected = choices(nonCollidedPossibleStates, weights=normalized_probs, k=1)[0]
        return selected

    def respawn(self, respawnPos):
        if self.superposition:
            self.collapseSuperposition()
        self.teleport(respawnPos)
        self.lives -= 1
        self.game.stateStack[-1].levelUI.updateCount('lives', -1)
        print(self.lives)
        if self.lives <= 0:
            self.game.stateStack[-1].level = 0
            self.lives = 3
            self.game.stateStack[-1].levelUI.resetCount(resetLives=True)
            self.game.stateStack[-1].loadLevel()
            self.game.stateStack[-1].levelUI.updateCount('lives', -1)

    def teleport(self, teleportPos):
        self.rect.topleft = teleportPos
        self.hitbox.topleft = teleportPos


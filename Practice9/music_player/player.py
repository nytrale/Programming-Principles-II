import os
import sys
import pygame


class MusicPlayer:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.width = 700
        self.height = 300
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Music Player")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("Arial", 28)
        self.small_font = pygame.font.SysFont("Arial", 22)

        self.tracks = self.load_tracks()
        self.current_index = 0
        self.is_playing = False

    def load_tracks(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        folder = os.path.join(base_dir, "music", "sample_tracks")
        tracks = []

        if os.path.exists(folder):
            for file_name in os.listdir(folder):
                if file_name.endswith(".mp3") or file_name.endswith(".wav"):
                    tracks.append(os.path.join(folder, file_name))

        tracks.sort()
        return tracks

    def play_track(self):
        if not self.tracks:
            return

        pygame.mixer.music.load(self.tracks[self.current_index])
        pygame.mixer.music.play()
        self.is_playing = True

    def stop_track(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next_track(self):
        if not self.tracks:
            return

        self.current_index = (self.current_index + 1) % len(self.tracks)
        self.play_track()

    def previous_track(self):
        if not self.tracks:
            return

        self.current_index = (self.current_index - 1) % len(self.tracks)
        self.play_track()

    def get_current_track_name(self):
        if not self.tracks:
            return "No tracks found"
        return os.path.basename(self.tracks[self.current_index])

    def draw_interface(self):
        self.screen.fill((245, 245, 245))

        title = self.font.render("Music Player", True, (0, 0, 0))
        self.screen.blit(title, (250, 20))

        track_text = self.small_font.render(
            f"Current track: {self.get_current_track_name()}",
            True,
            (0, 0, 0)
        )
        self.screen.blit(track_text, (50, 90))

        status = "Playing" if self.is_playing else "Stopped"
        status_text = self.small_font.render(f"Status: {status}", True, (0, 0, 0))
        self.screen.blit(status_text, (50, 130))

        controls = [
            "P - Play",
            "S - Stop",
            "N - Next track",
            "B - Previous track",
            "Q - Quit"
        ]

        y = 180
        for line in controls:
            text = self.small_font.render(line, True, (40, 40, 40))
            self.screen.blit(text, (50, y))
            y += 30

        if not self.tracks:
            warn = self.small_font.render(
                "Put mp3 or wav files into music/sample_tracks",
                True,
                (200, 0, 0)
            )
            self.screen.blit(warn, (50, 260))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.play_track()
                    elif event.key == pygame.K_s:
                        self.stop_track()
                    elif event.key == pygame.K_n:
                        self.next_track()
                    elif event.key == pygame.K_b:
                        self.previous_track()
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

            self.draw_interface()
            pygame.display.flip()
            self.clock.tick(30)
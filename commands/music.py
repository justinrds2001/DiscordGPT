import discord
from discord.ext import commands
import yt_dlp

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice = None
        self.queue = []
        self.playing = False
        self.next = None

    def get_next_song(self):
        if self.queue:
            self.next = self.queue.pop(0)
        else:
            self.next = None

    def play_next_song(self, error=None):
        try:
            if error:
                print(error)
            if self.next:
                source = self.next['source']
                self.voice.play(source, after=lambda e: self.play_next_song(e))
                self.playing = True
                self.get_next_song()
            else:
                self.playing = False
        except Exception as e:
            print(e)

    @commands.command()
    async def join(self, ctx):
        """Joins a voice channel"""
        if ctx.author.voice is None:
            await ctx.send("You must be in a voice channel to use this command.")
        self.voice = await ctx.author.voice.channel.connect()

    @commands.command()
    async def leave(self, ctx):
        """Leaves a voice channel"""
        await self.voice.disconnect()

    @commands.command()
    async def play(self, ctx, url):
        """Plays a song from a URL"""
        if not ctx.author.voice:
            await ctx.send("You are not connected to a voice channel.")
            return
        else:
            channel = ctx.author.voice.channel

        # Connect to the voice channel
        voice_client = ctx.voice_client
        if not voice_client:
            voice_client = await channel.connect()
            self.voice = voice_client
        else:
            await voice_client.move_to(channel)
            self.voice = voice_client

        # Download and play the audio
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }],
            'verbose': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            source = discord.FFmpegPCMAudio(info['url'])
            self.queue.append({'source': source, 'title': info['title']})
            if not self.playing:
                self.get_next_song()
                self.play_next_song()

        # Send a message to confirm that the audio is playing
        await ctx.send(f"Playing **{info['title']}** in {channel.name}.")


    @commands.command()
    async def pause(self, ctx):
        """Pauses the current song"""
        if self.voice.is_playing():
            self.voice.pause()
            await ctx.send("Playback paused.")
        else:
            await ctx.send("Playback is not currently active.")

    @commands.command()
    async def resume(self, ctx):
        """Resumes the current song"""
        if self.voice.is_paused():
            self.voice.resume()
            await ctx.send("Playback resumed.")
        else:
            await ctx.send("Playback is not currently paused.")

    @commands.command()
    async def skip(self, ctx):
        """Skips the current song"""
        if self.playing:
            self.voice.stop()
            await ctx.send("Skipping to next song.")
            self.get_next_song()
            self.play_next_song()
        else:
            await ctx.send("Playback is not currently active.")

    @commands.command()
    async def queue(self, ctx):
        """Shows the current queue"""
        if self.queue:
            message = "Current queue:\n"
            for i, song in enumerate(self.queue, start=1):
                message += f"{i}. {song['title']}\n"
            await ctx.send(message)
        else:
            await ctx.send("The queue is currently empty.")

async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))
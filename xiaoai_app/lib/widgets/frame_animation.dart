import 'package:flutter/material.dart';

/// Plays a sequence of frame images as a looping animation.
class FrameAnimation extends StatefulWidget {
  final String framesDir; // e.g. "frames/living_room_sitting_smile"
  final int frameCount;
  final int fps;
  final BoxFit fit;

  const FrameAnimation({
    super.key,
    required this.framesDir,
    required this.frameCount,
    this.fps = 12,
    this.fit = BoxFit.contain,
  });

  @override
  State<FrameAnimation> createState() => _FrameAnimationState();
}

class _FrameAnimationState extends State<FrameAnimation>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;
  int _currentFrame = 0;

  @override
  void initState() {
    super.initState();
    final duration = Duration(
      milliseconds: (widget.frameCount * 1000 / widget.fps).round(),
    );
    _controller = AnimationController(vsync: this, duration: duration)
      ..addListener(_onTick)
      ..repeat();
  }

  void _onTick() {
    final frame = (_controller.value * widget.frameCount).floor();
    final clamped = frame.clamp(0, widget.frameCount - 1);
    if (clamped != _currentFrame) {
      setState(() => _currentFrame = clamped);
    }
  }

  String get _framePath {
    final idx = (_currentFrame + 1).toString().padLeft(4, '0');
    return 'assets/${widget.framesDir}/frame_$idx.png';
  }

  @override
  Widget build(BuildContext context) {
    return Image.asset(
      _framePath,
      fit: widget.fit,
      gaplessPlayback: true, // prevents flicker between frames
      errorBuilder: (_, __, ___) => const SizedBox.shrink(),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }
}

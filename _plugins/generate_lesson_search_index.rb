require 'json'
require 'yaml'
require 'fileutils'

module Jekyll
  class LessonSearchIndexGenerator < Generator
    safe true
    priority :low

    def generate(site)
      source_dir = File.join(site.source, 'pages', 'ss_lessons')
      output_dir = File.join(site.dest, 'pages', 'ss_lessons')
      FileUtils.mkdir_p(output_dir)

      lesson_files = Dir.glob(File.join(source_dir, '*.md')).sort.reject do |path|
        File.basename(path) == 'index.md' || File.basename(path) == 'example.md'
      end

      records = lesson_files.map do |path|
        content = File.read(path)
        front_matter, body = split_front_matter(content)
        data = front_matter || {}

        {
          'title' => data['title'] || File.basename(path, '.md'),
          'slug' => File.basename(path, '.md'),
          'path' => File.basename(path),
          'quarter' => data['quarter'] || '',
          'week' => data['week'] || '',
          'season' => data['season'] || '',
          'description' => data['description'] || '',
          'theme' => data['theme'] || '',
          'memory_verse' => data['memory-verse'] || '',
          'page' => data['page'] || '',
          'content' => strip_markdown(body)
        }
      end

      json_content = JSON.pretty_generate(records)
      write_json(File.join(source_dir, 'lessons-search-index.json'), json_content)
      write_json(File.join(output_dir, 'lessons-search-index.json'), json_content)
    end

    private

    def split_front_matter(content)
      return [nil, content] unless content.start_with?("---\n") || content.start_with?("---\r\n")

      parts = content.split(/^---\s*$/m, 3)
      return [nil, content] unless parts.length >= 3

      front_matter = parts[1]
      body = parts[2].to_s.lstrip("\n").lstrip("\r")
      [YAML.safe_load(front_matter, permitted_classes: [Date, Time], aliases: true) || {}, body]
    rescue Psych::SyntaxError
      [nil, content]
    end

    def strip_markdown(text)
      text = text.gsub(/<!--.*?-->/m, '')
      text = text.gsub(/`([^`]*)`/, '\\1')
      text = text.gsub(/\[(.*?)\]\((.*?)\)/, '\\1')
      text = text.gsub(/[\#>*_~]/, ' ')
      text = text.gsub(/\s+/, ' ').strip
      text
    end

    def write_json(path, content)
      File.write(path, content)
    end
  end
end

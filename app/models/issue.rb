class Issue < ActiveRecord::Base
  attr_accessible :is_published, :number, :season, :title, :description, :prompt
  has_many :pieces
  has_many :illustrations, :through => :pieces
  has_many :authors, :through => :pieces
  has_many :illustrators, :through => :illustrations, :source => :author
  validates_presence_of :number, :title, :season
  validates_inclusion_of :is_published, :in => [true, false]
  before_save :publish_first_time_authors

  def url
    '/' + URLify.urlify(self.title, '-')
  end

  protected
    def publish_first_time_authors
      puts 'made it into publish_first_time_authors'
      if self.is_published
        # after issue updated, update any authors in issue who are newly published
        puts 'authors'
        puts self.authors
        self.authors.where(is_published: false).update_all(is_published: true)
        self.illustrators.where(is_published: false).update_all(is_published: true)
      else
        # unpublish authors that have pieces/illustrations only in this issue
        self.authors.each do |a|
          auth_issues = a.pieces.map{|p| p.issue.id} + a.illustrations.map{|p| p.issue.id}
          if auth_issues.uniq == [self.id]
            a.is_published = false
            a.save!
          end
        end
      end
    end
end

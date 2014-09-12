class Issue < ActiveRecord::Base
  attr_accessible :is_published, :number, :season, :title, :description, :prompt
  has_many :pieces
  has_many :illustrations, :through => :pieces
  has_many :authors, :through => :pieces
  validates_presence_of :number, :title, :season
  validates_inclusion_of :is_published, :in => [true, false]
  
  def url
    '/'+URLify.urlify(self.title,'-')
  end

  # TODO - after published updated, update any authors in issue who are newly published
end

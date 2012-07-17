class Issue < ActiveRecord::Base
  attr_accessible :is_published, :number, :season, :title, :description
  has_many :pieces
  has_many :authors, :through => :pieces
  def path
    urlify(self.title)
  end
end
